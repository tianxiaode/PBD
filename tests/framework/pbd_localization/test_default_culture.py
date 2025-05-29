import threading
import unittest
from pbd_localization import DefaultCulture, CultureInfo

en_info = CultureInfo(language_code='en', display_name='English', name='English', country_code='US')
fr_info = CultureInfo(language_code='fr', display_name='French', name='Français', country_code='FR')

class TestDefaultCulture(unittest.TestCase):

    def setUp(self):
        self.default_culture = DefaultCulture()
        self.default_culture._cultures = {}
        self.default_culture._default_code = None

    def test_singleton_pattern(self):
        instance1 = DefaultCulture()
        instance2 = DefaultCulture()
        self.assertIs(instance1, instance2)

    def test_thread_safe_singleton(self):
        def get_instance():
            return DefaultCulture()
        
        threads = [threading.Thread(target=get_instance) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        instances = {get_instance() for _ in range(10)}
        self.assertEqual(len(instances), 1)

    def test_initial_state(self):
        self.assertEqual(self.default_culture._cultures, {})
        self.assertIsNone(self.default_culture._default_code)

    def test_add_culture(self):
        culture = en_info
        self.default_culture.add(culture)
        self.assertIn('en', self.default_culture._cultures)
        self.assertEqual(self.default_culture._default_code, 'en')

        info = self.default_culture.get('en')
        self.assertEqual(info, culture)

    def test_add_multiple_cultures(self):
        culture1 = en_info
        culture2 = fr_info
        self.default_culture.add(culture1)
        self.default_culture.add(culture2)
        self.assertIn('en', self.default_culture._cultures)
        self.assertIn('fr', self.default_culture._cultures)
        self.assertEqual(self.default_culture._default_code, 'en')

        all = self.default_culture.get_all()
        self.assertEqual(all, {'en': culture1, 'fr': culture2})

    def test_set_default_after_add(self):
        culture1 = en_info
        culture2 = fr_info
        self.default_culture.add(culture1)
        self.default_culture.add(culture2)
        self.default_culture.set_default('fr')
        self.assertEqual(self.default_culture._default_code, 'fr')

    def test_get_default(self):
        culture = en_info
        self.default_culture.add(culture)
        self.default_culture.set_default('en')
        self.assertEqual(self.default_culture.get_default(), culture)

    def test_get_default_none(self):
        self.assertIsNone(self.default_culture.get_default())

    def test_remove_culture(self):
        culture = en_info
        self.default_culture.add(culture)
        self.default_culture.remove('en')
        self.assertNotIn('en', self.default_culture._cultures)
        self.assertIsNone(self.default_culture._default_code)

    def test_remove_culture_with_default(self):
        culture1 = en_info
        culture2 = fr_info
        self.default_culture.add(culture1)
        self.default_culture.add(culture2)
        self.default_culture.set_default('en')
        self.default_culture.remove('en')
        self.assertNotIn('en', self.default_culture._cultures)
        self.assertEqual(self.default_culture._default_code, 'fr')

    def test_has_culture(self):
        culture = en_info
        self.default_culture.add(culture)
        self.assertTrue(self.default_culture.has('en'))

    def test_has_culture_false(self):
        self.assertFalse(self.default_culture.has('en'))

if __name__ == '__main__':
    unittest.main()