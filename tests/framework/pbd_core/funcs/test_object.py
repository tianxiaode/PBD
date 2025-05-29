import unittest
from pbd_core import get_subclasses, get_all_subclasses

class TestGetSubclasses(unittest.TestCase):
    def test_get_subclasses_no_subclasses(self):
        class A: pass
        self.assertEqual(get_subclasses(A), [])
    
    def test_get_subclasses_with_subclasses(self):
        class A: pass
        class B(A): pass
        class C(A): pass
        
        result = get_subclasses(A)
        self.assertEqual(len(result), 2)
        self.assertIn(B, result)
        self.assertIn(C, result)
    
    def test_get_all_subclasses_no_subclasses(self):
        class A: pass
        self.assertEqual(get_all_subclasses(A), [])
    
    def test_get_all_subclasses_one_level(self):
        class A: pass
        class B(A): pass
        class C(A): pass
        
        result = get_all_subclasses(A)
        self.assertEqual(len(result), 2)
        self.assertIn(B, result)
        self.assertIn(C, result)
    
    def test_get_all_subclasses_multiple_levels(self):
        class A: pass
        class B(A): pass
        class C(B): pass
        class D(C): pass
        
        result = get_all_subclasses(A)
        self.assertEqual(len(result), 3)
        self.assertIn(B, result)
        self.assertIn(C, result)
        self.assertIn(D, result)

if __name__ == '__main__':
    unittest.main()

