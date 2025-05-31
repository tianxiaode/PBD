import unittest
from pbd_core import Extendable


class TestExtendable(unittest.TestCase):
    def setUp(self):
        Extendable._extensions = {}
        Extendable._extension_params = {}

    def test_register_with_no_target_type(self):
        class TestClass(Extendable):
            pass

        @TestClass.register()
        def test_extension(self: TestClass, **kwargs):
            self.test_attr = kwargs.get('test_attr', None)

        instance = TestClass(test_attr='value')
        self.assertTrue(hasattr(instance, 'test_attr'))
        self.assertEqual(instance.test_attr, 'value')

    def test_register_with_target_type(self):
        class BaseClass(Extendable):
            pass

        class TestClass(BaseClass):
            pass

        @BaseClass.register(target_type=TestClass)
        def test_extension(self: TestClass, **kwargs):
            self.test_attr = kwargs.get('test_attr', None)

        instance = TestClass(test_attr='value')
        self.assertTrue(hasattr(instance, 'test_attr'))
        self.assertEqual(instance.test_attr, 'value')


