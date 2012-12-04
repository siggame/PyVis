import unittest
from mock import patch, MagicMock, call

import gameloader

class TestGameLoader(unittest.TestCase):
    def test_determine_type(self):

        gz_file = '\x1f\x8b\x08blahblabahblkjdflakfjlafa'
        bz2_file = '\x42\x5a\x68gobbeldygook'
        zips = [
            '\x50\x4b\x07lakjdfalsdfasfda',
            '\x50\x4b\x05lakjdfalsdfasfda',
            '\x50\x4b\x04lakjdfalsdfasfda',
            '\x50\x4b\x03lakjdfalsdfasfda'
            ]

        app = MagicMock()
        loader = gameloader.GameLoader(app)

        self.assertEqual(loader.determine_type(gz_file), 'gz')
        self.assertEqual(loader.determine_type(bz2_file), 'bz2')
        for z in zips:
            self.assertEqual(loader.determine_type(z), 'zip')

        self.assertEqual(loader.determine_type(gz_file[:3]), 'gz')
        self.assertEqual(loader.determine_type(bz2_file[:3]), 'bz2')
        for z in zips:
            self.assertEqual(loader.determine_type(z[:3]), 'zip')

        self.assertEqual(loader.determine_type(gz_file[:2]), 'json')
        self.assertEqual(loader.determine_type(bz2_file[:2]), 'json')
        for z in zips:
            self.assertEqual(loader.determine_type(z[:2]), 'json')

        self.assertEqual(loader.determine_type('{"json": "file"}'), 'json')

        self.assertEqual(loader.determine_type('a' + bz2_file), 'json')

    @patch('gameloader.StringIO')
    @patch('zipfile.ZipFile')
    @patch('gzip.GzipFile')
    @patch('bz2.decompress')
    def test_decompress(self, bz2, gzip, zip, strio):
        app = MagicMock()
        loader = gameloader.GameLoader(app)

        bz2.return_value = 'decompressed_bz2'
        self.assertIsNone(loader.decompress('data', 'bz2'))
        bz2.assert_called_once_with('data')
        app.queue_log.assert_called_once_with('decompressed_bz2')

        strio.return_value = 'io_data'
        gz = MagicMock()
        gz.read.return_value = 'decompressed_gz'
        gzip.return_value = gz
        self.assertIsNone(loader.decompress('data', 'gz'))
        strio.assert_called_once_with('data')
        gzip.assert_called_once_with(filename='bogus.glog', mode='rb', fileobj='io_data')
        self.assertEqual(app.queue_log.mock_calls[1], call('decompressed_gz'))

        z = MagicMock()
        z.namelist.return_value = ['a', 'b']
        z.read.return_value = 'decompressed_zip'
        zip.return_value = z
        self.assertIsNone(loader.decompress('data', 'zip'))
        zip.assert_called_once_with('io_data', 'r')

        self.assertEqual(z.read.mock_calls[0], call('a'))
        self.assertEqual(z.read.mock_calls[1], call('b'))

        self.assertEqual(app.queue_log.mock_calls[2], call('decompressed_zip'))
        self.assertEqual(app.queue_log.mock_calls[3], call('decompressed_zip'))

        with self.assertRaises(Exception):
            loader.decompress('data', 'unknown')

    @patch('gameloader.GameLoader.decompress')
    @patch('gameloader.GameLoader.determine_type')
    @patch('gameloader.open', create=True)
    def test_load(self, op, dt, decompress):
        app = MagicMock()
        loader = gameloader.GameLoader(app)

        def read_effect(*args):
            if len(args):
                return 'start'
            else:
                return 'output stuff'

        file_mock = MagicMock()
        op.return_value.__enter__.return_value = file_mock
        file_mock.read.side_effect = read_effect

        dt.return_value = 'json'
    
        self.assertIsNone(loader.load('path'))
        self.assertEqual(op.mock_calls[0], call('path'))
        self.assertEqual(file_mock.read.mock_calls[0], call(3))
        dt.assert_called_with('start')
        # calls 1-3 are __open__(), read(), and __exit__()
        self.assertEqual(op.mock_calls[4], call('path', 'r'))
        app.queue_log.assert_called_once_with('output stuff')

        dt.return_value = 'zip'
        self.assertIsNone(loader.load('path2'))
        self.assertEqual(op.mock_calls[8], call('path2'))
        self.assertEqual(file_mock.read.mock_calls[2], call(3))
        dt.assert_called_with('start')
        self.assertEqual(op.mock_calls[12], call('path2', 'rb'))
        self.assertEqual(file_mock.read.mock_calls[3], call())
        decompress.assert_called_once_with('output stuff', 'zip')

    @patch('gameloader.GameLoader.decompress')
    @patch('gameloader.GameLoader.determine_type')
    def test_loads(self, dt, decompress):
        app = MagicMock()
        loader = gameloader.GameLoader(app)

        dt.return_value = 'json'
        loader.max_len = 6
        self.assertIsNone(loader.loads('input glog data'))
        dt.assert_called_once_with('input ')
        app.queue_log.assert_called_once_with('input glog data')

        dt.return_value = 'zip'
        loader.max_len = 4
        self.assertIsNone(loader.loads('other glog data'))
        self.assertEqual(dt.mock_calls[1], call('othe'))
        decompress.assert_called_once_with('other glog data', 'zip')
