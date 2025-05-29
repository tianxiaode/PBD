import unittest
from unittest.mock import patch, MagicMock
from pbd_localization import DefaultLocalizer

class TestDefaultLocalizer(unittest.TestCase):

    def setUp(self):
        self.localizer = DefaultLocalizer()
        self.localizer.set_current_lang('en')

    @patch('pbd_localization.default_localizer.LocalizationResource.get')
    def test_get_single_key(self, mock_get):
        mock_get.return_value = 'Hello'
        result = self.localizer.get('hello_key')
        self.assertEqual(result, 'Hello')

    @patch('pbd_localization.default_localizer.LocalizationResource.get')
    def test_get_multiple_keys(self, mock_get):
        mock_get.return_value = 'Hello World'
        result = self.localizer.get(['hello_key', 'world_key'])
        self.assertEqual(result, 'Hello World')

    @patch('pbd_localization.default_localizer.LocalizationResource.get')
    def test_get_with_default(self, mock_get):
        mock_get.return_value = 'Default Message'
        result = self.localizer.get('nonexistent_key', default='Default Message')
        self.assertEqual(result, 'Default Message')

    @patch('pbd_localization.default_localizer.LocalizationResource.get')
    def test_get_with_default_none(self, mock_get):
        mock_get.return_value = None
        result = self.localizer.get('nonexistent_key', default=None)
        self.assertIsNone(result)

    @patch('pbd_localization.default_localizer.LocalizationResource.get')
    def test_get_with_default_empty_string(self, mock_get):
        mock_get.return_value = ''
        result = self.localizer.get('empty_string_key', default='Default Message')
        self.assertEqual(result, '')

    @patch('pbd_localization.default_localizer.LocalizationResource.get')
    def test_get_no_default(self, mock_get):
        mock_get.return_value = None
        result = self.localizer.get('nonexistent_key')
        self.assertIsNone(result)

    @patch('pbd_localization.default_localizer.LocalizationResource.get')
    def test_get_single_key_with_empty_string(self, mock_get):
        mock_get.return_value = ''
        result = self.localizer.get('empty_string_key')
        self.assertEqual(result, '')

    @patch('pbd_localization.default_localizer.LocalizationResource.get')
    def test_get_multiple_keys_with_empty_string(self, mock_get):
        mock_get.return_value = ''        
        result = self.localizer.get(['empty_string_key', 'another_empty_key'])
        self.assertEqual(result, '')

    @patch('pbd_localization.default_localizer.LocalizationResource.get')
    def test_get_multiple_keys_with_mixed_values(self, mock_get):
        mock_get.side_effect = ['Hello', None, 'World']
        result = self.localizer.get(['key1', 'key2', 'key3'])
        self.assertEqual(result, 'Hello')

    @patch('pbd_localization.default_localizer.LocalizationResource.get')
    def test_get_multiple_keys_with_all_none(self, mock_get):
        mock_get.return_value = None
        result = self.localizer.get(['key1', 'key2', 'key3'])
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()