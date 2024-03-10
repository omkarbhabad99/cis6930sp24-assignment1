import unittest
from censoror import censor_document

class TestNames(unittest.TestCase):
    def test_censor_single_name(self):
        text = "John went to the park."
        # Modified line below
        censored_text = censor_document(text, {'PERSON'}, {'NAMES': 0, 'DATES': 0, 'ADDRESSES': 0, 'PHONE_NUMBERS': 0})
        self.assertEqual(censored_text, "████ went to the park.")

    def test_censor_full_name(self):
        text = "Sarah Connor was here."
        # Modified line below
        censored_text = censor_document(text, {'PERSON'}, {'NAMES': 0, 'DATES': 0, 'ADDRESSES': 0, 'PHONE_NUMBERS': 0})
        self.assertEqual(censored_text, "████████████ was here.")

if __name__ == '__main__':
    unittest.main()

