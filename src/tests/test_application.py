import unittest
from mock import patch, MagicMock, call
import sys

import application


class TestApplication(unittest.TestCase):
    @patch('gameloader.GameLoader')
    @patch('application.Window')
    def test_init(self, mock_win, loader):

        mock_win.WINDOW_STYLE_DEFAULT=-24

        app = application.Application((1, 3), 'test title', True)

        mock_win.assert_called_with(width=1, height=3, caption='test title', 
                visible=True, fullscreen=True, resizable=True, 
                style=-24, vsync=False, display=None,
                context=None, config=None)

        self.assertEqual(len(app.updates), 0)
        self.assertTrue(app.need_new_log)
        self.assertEqual(app.queue_idx, 0)
        loader.assert_called_once_with(app)

        app = application.Application()
        mock_win.assert_called_with(width=640, height=480, 
                caption='MegaMinerAI Bland Title Text',
                visible=True, fullscreen=False, resizable=True, 
                style=-24, vsync=False, display=None,
                context=None, config=None)

        loader.assert_called_with(app)

    @patch('application.Window')
    def test_request_update_on_draw(self, mock_win):
        app = application.Application()
        self.assertEqual(len(app.updates), 0)

        app.request_update_on_draw('b')
        self.assertListEqual(app.updates, [(50, 'b')])
 
        app.request_update_on_draw('c', -23)
        self.assertListEqual(app.updates, [(-23, 'c'), (50, 'b')])
        app.request_update_on_draw('d', 0)
        app.request_update_on_draw('e', 100)
        self.assertListEqual(app.updates, 
                [(-23, 'c'), (0, 'd'), (50, 'b'), (100, 'e')])

    @patch('application.Application.play_log')
    @patch('application.Window')
    def test_update(self, mock_win, play_log):
        app = application.Application()

        func1, func2, func3 = MagicMock(), MagicMock(), MagicMock()

        app._update(4)
        self.assertEqual(app.window.clear.call_count, 1)

        # Make sure the functions start in an uncalled state
        for i in [func1, func2, func3]:
            self.assertFalse(i.called)

        # add them to the update request list
        app.updates = [(0, func1), (24, func2), (85, func3)]

        app._update(5)

        # Make sure all the functions have been called exactly once
        for i in [func1, func2, func3]:
            self.assertEqual(i.call_count, 1)

        # Make sure no log has been played yet
        self.assertFalse(play_log.called)
        self.assertTrue(app.need_new_log)
        self.assertEqual(app.queue_idx, 0)
        self.assertEqual(len(app.log_queue), 0)

        # Load up the log_queue simulating a file->open()
        app.log_queue = ['logA', 'logB', 'logC']
        app._update(5)
        self.assertEqual(app.queue_idx, 1)
        self.assertEqual(len(app.log_queue), 3)
        self.assertTrue(play_log.called)

        play_log.assert_called_once_with('logA')
        app._update(2)
        self.assertEqual(play_log.call_count, 2)
        self.assertEqual(play_log.mock_calls[1], call('logB'))
        self.assertEqual(app.queue_idx, 2)

        app.need_new_log = False
        app._update(1)
        self.assertEqual(play_log.call_count, 2)
        self.assertEqual(app.queue_idx, 2)

        app.need_new_log = True
        app._update(1)
        self.assertEqual(play_log.call_count, 3)
        self.assertEqual(play_log.mock_calls[2], call('logC'))
        self.assertEqual(app.queue_idx, 3)

        app._update(1)
        self.assertEqual(play_log.call_count, 3)
        self.assertEqual(app.queue_idx, 3)

    @patch('os.path.join')
    @patch('application.config')
    @patch('imp.load_source')
    @patch('application.Window')
    def test_play_log(self, mock_win, load_source, config, path_join):
        app = application.Application()

        config.PLUGIN_DIR = 'dir1'
        path_join.return_value = 'dir1/game1/main.py'

        game = MagicMock()

        load_source.return_value = game

        log = {'gameName': 'GAME1'}
        app.play_log(log)

        path_join.assert_called_once_with('dir1', 'game1', 'main.py')

        load_source.assert_called_once_with('game1', 'dir1/game1/main.py')

        game.load.assert_called_once_with(app, {'gameName': 'GAME1'})

    @patch('application.json')
    @patch('application.Window')
    @patch('application.config')
    def test_queue_log(self, config, mock_win, json):

        config.PLUGIN_DIR = 'dir1'
        app = application.Application()
        json.loads.return_value = {'gameName': 'dir2'}

        app.queue_log('json_data')

        self.assertListEqual(app.log_queue, [{'gameName': 'dir2'}])

        # application.os.path.join.return_value = 'dir1/dir2/main.py'
        # application.os.path.join.assert_called_once_with('dir1', 'dir2', 'main.py')

        # json.loads.called_once_with('json_data')

    @patch('application.gameloader')
    @patch('application.Window')
    @patch('application.pyglet')
    def test_run(self, pyglet, mock_win, gameloader):

        app = application.Application()

        app.run()

        self.assertFalse(app.loader.load.called)

        app.run(['1.glog', '6.glog', '3.glog']) 

        self.assertEqual(app.loader.load.call_count, 3)

        self.assertEqual(pyglet.clock.schedule.call_count, 2)
        self.assertEqual(pyglet.app.run.call_count, 2)

