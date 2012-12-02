import unittest
from mock import patch
import sys

sys.path.append('..')
import application


class TestApplication(unittest.TestCase):
    @patch('pyglet.window')
    def test_init(self, mock_win):
        app = application.Application()

        print(mock_win.method_calls)
        #print(mock_win.__init__.call_count)
        #mock_win.assert_called_with(


if __name__ == '__main__':
    unittest.main()
