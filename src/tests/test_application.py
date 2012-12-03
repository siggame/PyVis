import unittest
from mock import patch, MagicMock
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
        loader.assert_called_once_with(app)

        app = application.Application()
        mock_win.assert_called_with(width=640, height=480, 
                caption='MegaMinerAI Bland Title Text',
                visible=True, fullscreen=False, resizable=True, 
                style=-24, vsync=False, display=None,
                context=None, config=None)

        loader.asser_called_once_with(app)

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

    @patch('application.Window')
    def test_update(self, mock_win):
        app = application.Application()

        func1, func2, func3 = MagicMock(), MagicMock(), MagicMock()

        app._update(4)
        self.assertEqual(app.window.clear.call_count, 1)

        for i in [func1, func2, func3]:
            self.assertFalse(i.called)

        app.updates = [(0, func1), (24, func2), (85, func3)]

        app._update(5)

        for i in [func1, func2, func3]:
            self.assertEqual(i.call_count, 1)

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

if __name__ == '__main__':
    unittest.main()
