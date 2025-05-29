import unittest
from unittest.mock import MagicMock
from pbd_localization import DefaultCultureStore,CultureInfo

class TestDefaultCultureStore(unittest.TestCase):
    def setUp(self):
        self.store = DefaultCultureStore()
        self.store._data = MagicMock()

    def test_initialize(self):
        self.store.initialize()
        self.assertIsNotNone(self.store._data)

    def test_get_all_happy_path(self):
        en_mock = MagicMock(spec=CultureInfo)
        zh_mock = MagicMock(spec=CultureInfo)
        self.store._data.get_all.return_value = {'en': en_mock, 'zh': zh_mock}
        result = self.store.get_all()
        self.assertEqual(result, {'en': en_mock, 'zh': zh_mock})

    def test_get_all_edge_case_empty(self):
        self.store._data.get_all.return_value = {}
        result = self.store.get_all()
        self.assertEqual(result, {})

    def test_get_happy_path(self):
        culture_info_mock = MagicMock()
        self.store._data.get.return_value = culture_info_mock
        result = self.store.get('en')
        self.assertEqual(result, culture_info_mock)

    def test_get_edge_case_not_found(self):
        self.store._data.get.return_value = None
        result = self.store.get('fr')
        self.assertIsNone(result)

    def test_add_happy_path(self):
        data = MagicMock(spec=CultureInfo)
        self.store.add(data)
        self.store._data.add.assert_called_once_with(data)

    def test_remove_happy_path(self):
        self.store.remove('en')
        self.store._data.remove.assert_called_once_with('en')

    def test_set_default_happy_path(self):
        self.store.set_default('en')
        self.store._data.set_default.assert_called_once_with('en')

    def test_get_default_happy_path(self):
        culture_info_mock = MagicMock()
        self.store._data.get_default.return_value = culture_info_mock
        result = self.store.get_default()
        self.assertEqual(result, culture_info_mock)

    def test_get_default_edge_case_not_set(self):
        self.store._data.get_default.return_value = None
        result = self.store.get_default()
        self.assertIsNone(result)

    def test_has_happy_path(self):
        self.store._data.get_all.return_value = {'en': MagicMock(), 'zh': MagicMock()}
        result = self.store.has()
        self.assertTrue(result)

    def test_has_edge_case_empty(self):
        self.store._data.get_all.return_value = {}
        result = self.store.has()
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()