import unittest
import uuid
from unittest.mock import patch
from pbd_guids import SequentialGuidGenerator

class TestSequentialGuidGenerator(unittest.TestCase):

    def setUp(self):
        self.guid_generator = SequentialGuidGenerator()

    def test_happy_path(self):
        guid1 = self.guid_generator.create()
        guid2 = self.guid_generator.create()
        self.assertIsInstance(guid1, uuid.UUID)
        self.assertIsInstance(guid2, uuid.UUID)
        self.assertNotEqual(guid1, guid2)

    def test_sequence_increment(self):
        with patch('time.time_ns', return_value=1609459200000000):
            guid1 = self.guid_generator.create()
        with patch('time.time_ns', return_value=1609459200000000):
            guid2 = self.guid_generator.create()
        self.assertNotEqual(guid1, guid2)

    def test_timestamp_increment_on_same_time(self):
        with patch('time.time_ns', return_value=1609459200000000):
            for _ in range(0x10000):
                self.guid_generator.create()
        with patch('time.time_ns', return_value=1609459200000000):
            guid1 = self.guid_generator.create()
        with patch('time.time_ns', return_value=1609459200000001):
            guid2 = self.guid_generator.create()
        self.assertNotEqual(guid1, guid2)

    def test_sequence_wraparound(self):
        with patch('time.time_ns', return_value=1609459200000000):
            for _ in range(0x10000):
                self.guid_generator.create()
            guid1 = self.guid_generator.create()
        with patch('time.time_ns', return_value=1609459200000001):
            guid2 = self.guid_generator.create()
        self.assertNotEqual(guid1, guid2)

    def test_timestamp_increment(self):
        with patch('time.time_ns', return_value=1609459200000000):
            guid1 = self.guid_generator.create()
        with patch('time.time_ns', return_value=1609459201000000):
            guid2 = self.guid_generator.create()
        self.assertNotEqual(guid1, guid2)

if __name__ == '__main__':
    unittest.main()