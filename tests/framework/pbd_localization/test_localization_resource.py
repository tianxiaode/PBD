import unittest
from unittest.mock import patch
from pbd_localization import LocalizationResource

class TestResource(LocalizationResource):
    resource_name = "test_resource"
    texts = {
        'en': {'hello': 'Hello', 'goodbye': 'Goodbye'},
        'zh-CN': {'hello': '你好', 'goodbye': '再见'}
    }

class TestLocalizationResource(unittest.TestCase):
    def setUp(self):
        self.text_resource = TestResource()
        

    def test_get_default_lang(self):
        self.assertEqual(LocalizationResource.get_default_lang(), "en")

    def test_set_default_lang(self):
        LocalizationResource.set_default_lang("fr")
        self.assertEqual(LocalizationResource.get_default_lang(), "fr")

    def test_set_default_lang_invalid_value(self):
        with self.assertRaises(ValueError):
            LocalizationResource.set_default_lang("")

        with self.assertRaises(ValueError):
            LocalizationResource.set_default_lang(None)
    
    def test_set_default_lang_no_base_class(self):
        with self.assertRaises(AttributeError):
            TestResource.set_default_lang("fr")        

    def test_get_with_valid_path(self):
        self.assertEqual(LocalizationResource.get("test_resource.hello", "en"), "Hello")
        self.assertEqual(LocalizationResource.get("test_resource.goodbye", "zh-CN"), "再见")

    def test_get_with_invalid_path(self):
        self.assertIsNone(LocalizationResource.get("test_resource.hello.world", "en"))
        self.assertIsNone(LocalizationResource.get("invalid_resource.hello", "en"))
    
    def test_get_with_one_key(self):
        self.assertEqual(LocalizationResource.get("test_resource", "en", 'default_value'), "default_value")

    def test_get_by_resource_name_with_valid_keys(self):
        self.assertEqual(LocalizationResource.get_by_resource_name("test_resource", "en", "hello"), "Hello")
        self.assertEqual(LocalizationResource.get_by_resource_name("test_resource", "zh-CN", ["goodbye"]), "再见")

    def test_get_by_resource_name_with_invalid_keys(self):
        self.assertIsNone(LocalizationResource.get_by_resource_name("test_resource", "en", "hello.world"))
        self.assertIsNone(LocalizationResource.get_by_resource_name("test_resource", "zh-CN", ["goodbye", "world"]))

    def test_get_resource_with_valid_resource(self):
        self.assertEqual(LocalizationResource.get_resource("test_resource", "en"), {'hello': 'Hello', 'goodbye': 'Goodbye'})
        self.assertEqual(LocalizationResource.get_resource("test_resource", "zh-CN"), {'hello': '你好', 'goodbye': '再见'})

    def test_get_resource_with_invalid_resource(self):
        self.assertEqual(LocalizationResource.get_resource("invalid_resource", "en"), {})

    def test_get_resources(self):
        self.assertEqual(LocalizationResource.get_resources("en"), {"test_resource": {'hello': 'Hello', 'goodbye': 'Goodbye'}})
        self.assertEqual(LocalizationResource.get_resources("zh-CN"), {"test_resource": {'hello': '你好', 'goodbye': '再见'}})

    def test_get_resources_with_default_lang(self):
        with patch.dict(self.text_resource.texts, {'fr': {'hello': 'Bonjour'}}):
            self.assertEqual(LocalizationResource.get_resources("fr"), {"test_resource": {'hello': 'Bonjour'}})
            self.assertEqual(LocalizationResource.get_resources("invalid"), {"test_resource": {'hello': 'Hello', 'goodbye': 'Goodbye'}})

    def test_validate_resource_with_empty_resource_name(self):
        with self.assertRaises(ValueError):
            class InvalidResource(LocalizationResource):
                resource_name = ""
                texts = {}

    def test_validate_texts_with_invalid_format(self):
        with self.assertRaises(ValueError):
            class InvalidTextsResource(LocalizationResource):
                resource_name = "invalid_texts"
                texts = "invalid_format"

        with self.assertRaises(ValueError):
            class InvalidTextsResource2(LocalizationResource):
                resource_name = "invalid_texts2"
                texts = {'en': 'invalid_format'}

        with self.assertRaises(ValueError):
            class InvalidTextsResource3(LocalizationResource):
                resource_name = "invalid_texts3"
                texts = {'en': {}, 'zh-CN': "invalid_format"}
    
    def test_duplicate_resource_name(self):
        with self.assertRaises(ValueError):
            class RepeatedResourceNameResource(LocalizationResource):
                resource_name = "test_resource"
                texts = {}

if __name__ == '__main__':
    unittest.main()