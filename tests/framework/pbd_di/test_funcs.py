import unittest
from pbd_di import replace_service

class TestReplaceService(unittest.TestCase):
    def test_happy_path(self):
        class SourceService:
            pass

        class TargetService:
            pass

        replace_service(SourceService, TargetService)
        self.assertTrue(hasattr(TargetService, '__di_implementation__'))
        self.assertEqual(TargetService.__di_implementation__, SourceService)

    def test_source_is_none(self):
        class TargetService:
            pass

        with self.assertRaises(TypeError):
            replace_service(None, TargetService)

    def test_target_is_none(self):
        class SourceService:
            pass

        with self.assertRaises(TypeError):
            replace_service(SourceService, None)

    def test_both_are_none(self):
        with self.assertRaises(TypeError):
            replace_service(None, None)

    def test_source_is_not_class(self):
        class TargetService:
            pass

        with self.assertRaises(TypeError):
            replace_service("not a class", TargetService)

    def test_target_is_not_class(self):
        class SourceService:
            pass

        with self.assertRaises(TypeError):
            replace_service(SourceService, "not a class")

    def test_both_are_not_class(self):
        with self.assertRaises(TypeError):
            replace_service("not a class", "also not a class")

    def test_source_and_target_are_same_class(self):
        class Service:
            pass

        replace_service(Service, Service)
        self.assertTrue(hasattr(Service, '__di_implementation__'))
        self.assertEqual(Service.__di_implementation__, Service)


if __name__ == '__main__':
    unittest.main()