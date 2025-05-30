import unittest
from unittest.mock import MagicMock
#from pbd_settings import SettingDefinitionProvider,Se



class TestSettingGroup(unittest.TestCase):

    def setUp(self):
        pass
        #SettingDefinitionProvider._registry = {}


    # def test_init_subclass_happy_path(self):
    #     class TestGroup(SettingDefinitionProvider):
    #         group_name = "test_group"
    #         settings = [SettingDefinition(name="test_setting", type=int, default_value=0)]

    #     self.assertIn("test_group.test_setting", SettingDefinitionProvider._registry)

    # def test_init_subclass_non_setting_definition(self):
    #     with self.assertRaises(TypeError):
    #         class TestGroup(SettingDefinitionProvider):
    #             group_name = "test_group"
    #             settings = [123]

    # def test_init_subclass_duplicate_setting(self):
    #     class TestGroup1(SettingDefinitionProvider):
    #         group_name = "test_group"
    #         settings = [SettingDefinition(name="test_setting", type=int, default_value=0)]

    #     with self.assertRaises(ValueError):
    #         class TestGroup2(SettingDefinitionProvider):
    #             group_name = "test_group"
    #             settings = [SettingDefinition(name="test_setting", type=int, default_value=0)]

    # def test_init_subclass_empty_settings(self):
    #     class TestGroup(SettingDefinitionProvider):
    #         group_name = "test_group"
    #         settings = []

    #     self.assertEqual(SettingDefinitionProvider._registry, {})

    # def test_init_subclass_multiple_settings(self):
    #     class TestGroup(SettingDefinitionProvider):
    #         group_name = "test_group"
    #         settings = [
    #             SettingDefinition(name="test_setting1", type=int, default_value=0),
    #             SettingDefinition(name="test_setting2", type=str, default_value="default_value")
    #         ]

    #     self.assertIn("test_group.test_setting1", SettingDefinitionProvider._registry)
    #     self.assertIn("test_group.test_setting2", SettingDefinitionProvider._registry)

    # def test_init_subclass_inheritance(self):
    #     class BaseGroup(SettingDefinitionProvider):
    #         group_name = "base_group"
    #         settings = [SettingDefinition(name="base_setting", type=int, default_value=0)]

    #     class DerivedGroup(BaseGroup):
    #         group_name = "derived_group"
    #         settings = [SettingDefinition(name="derived_setting", type=str, default_value="default_value")]

    #     self.assertIn("base_group.base_setting", SettingDefinitionProvider._registry)
    #     self.assertIn("derived_group.derived_setting", SettingDefinitionProvider._registry)

    # def test_init_subclass_dynamic_setting(self):
    #     class DynamicGroup(SettingDefinitionProvider):
    #         group_name = "dynamic_group"
    #         settings = [SettingDefinition(name="dynamic_setting", type=int, default_value=MagicMock())]

    #     self.assertIn("dynamic_group.dynamic_setting", SettingDefinitionProvider._registry)

    # def test_get_settings(self):
    #     class TestGroup(SettingDefinitionProvider):
    #         group_name = "test_group"
    #         settings = [SettingDefinition(name="test_setting", type=int, default_value=0)]
    #     settings = SettingDefinitionProvider.get_settings()
    #     self.assertIn("test_group.test_setting", settings)
    #     self.assertEqual(settings["test_group.test_setting"].default_value, 0)
    
    # def tset_get_setting(self):
    #     class TestGroup(SettingDefinitionProvider):
    #         group_name = "test_group"
    #         settings = [SettingDefinition(name="test_setting", type=int, default_value=0)]
    #     setting = SettingDefinitionProvider.get_setting('test_group.test_setting')
    #     self.assertEqual(setting.default_value, 0)

    # def test_get_setting_non_existent(self):
    #     class TestGroup(SettingDefinitionProvider):
    #         group_name = "test_group"
    #         settings = [SettingDefinition(name="test_setting", type=int, default_value=0)]
    #     setting = SettingDefinitionProvider.get_setting('test_group.test_setting1')
    #     self.assertEqual(setting, None)

    # def test_setting_definition_normalize_type(self):
    #     class TestGroup(SettingDefinitionProvider):
    #         group_name = "test_group"
    #         settings = [SettingDefinition(name="test_setting", type='int', default_value=0)]
    #     setting = SettingDefinitionProvider.get_setting('test_group.test_setting')
    #     self.assertEqual(setting.type,int.__name__)


if __name__ == '__main__':
    unittest.main()