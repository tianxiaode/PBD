import logging
import unittest
from unittest.mock import patch, MagicMock
from pbd_core import HasLogger

class TestHasLogger(unittest.TestCase):

    def test_logger_happy_path(self):
        with patch('pbd_core.logging.Logger.get_logger') as mock_get_logger:
            mock_logger = MagicMock(spec=logging.Logger)
            mock_get_logger.return_value = mock_logger

            has_logger_instance = HasLogger()
            self.assertEqual(has_logger_instance.logger, mock_logger)
            mock_get_logger.assert_called_once_with(has_logger_instance.__class__)

    def test_logger_already_set(self):
        with patch('pbd_core.logging.Logger.get_logger') as mock_get_logger:
            mock_logger = MagicMock(spec=logging.Logger)
            mock_get_logger.return_value = mock_logger

            has_logger_instance = HasLogger()
            has_logger_instance._logger = mock_logger
            self.assertEqual(has_logger_instance.logger, mock_logger)
            mock_get_logger.assert_not_called()

    def test_logger_class_method_called_once(self):
        with patch('pbd_core.logging.Logger.get_logger') as mock_get_logger:
            mock_logger = MagicMock(spec=logging.Logger)
            mock_get_logger.return_value = mock_logger

            has_logger_instance = HasLogger()
            _ = has_logger_instance.logger
            _ = has_logger_instance.logger
            mock_get_logger.assert_called_once_with(has_logger_instance.__class__)

if __name__ == '__main__':
    unittest.main()