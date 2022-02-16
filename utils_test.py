import unittest

from utils import generate_uuid

class UtilsTest(unittest.TestCase):

    def test_uuid(self):
        print(generate_uuid())
        self.assertEqual(len(generate_uuid()), 32)