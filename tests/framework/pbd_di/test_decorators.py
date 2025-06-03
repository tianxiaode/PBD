import unittest
from unittest.mock import MagicMock, patch
from pbd_di import injectable_extension, ITransientDependency, InjectableExtensionInvalidTypeException


class ExtensionModule:
    def new_method(self):
        return "new_method"

class TestInjectableExtension(unittest.TestCase):

    def setUp(self):
        self.targetClass = type('TargetClass', (ITransientDependency,), {})
        self.MockService1 = type('MockService1', (ITransientDependency,), {})
        self.MockService2 = type('MockService2', (ITransientDependency,), {})

    def test_happy_path(self):
        TargetClass = self.targetClass
        injectable_extension(TargetClass, [self.MockService1, self.MockService2])(ExtensionModule)
        self.assertIn(self.MockService1, TargetClass.deps.values())
        self.assertIn(self.MockService2, TargetClass.deps.values())
        self.assertTrue(callable(getattr(TargetClass, 'new_method')))

    def test_no_deps(self):
        TargetClass = self.targetClass
        injectable_extension(TargetClass)(ExtensionModule)
        self.assertDictEqual(TargetClass.deps, {})
        self.assertTrue(callable(getattr(TargetClass, 'new_method')))

    def test_empty_deps(self):
        TargetClass = self.targetClass
        injectable_extension(TargetClass, [])(ExtensionModule)
        self.assertEqual(len(TargetClass.deps.keys()), 0)
        self.assertTrue(callable(getattr(TargetClass, 'new_method')))

    def test_non_dependency_base_class(self):
        class NonDependencyBase:
            pass

        with self.assertRaises(InjectableExtensionInvalidTypeException) as context:
            injectable_extension(NonDependencyBase)(ExtensionModule)
        self.assertIsInstance(context.exception, InjectableExtensionInvalidTypeException)

    def test_existing_method_overwrite(self):
        TargetClass = self.targetClass
        class ExistingMethodModule:
            def new_method(self):
                return "existing_method"

        injectable_extension(TargetClass, [self.MockService1])(ExistingMethodModule)
        self.assertTrue(callable(getattr(TargetClass, 'new_method')))

    def test_special_methods_not_injected(self):
        TargetClass = self.targetClass
        class SpecialMethodModule:
            def __special_method__(self):
                return "special_method"

        injectable_extension(TargetClass, [self.MockService1])(SpecialMethodModule)
        self.assertNotIn('__special_method__', dir(TargetClass))
