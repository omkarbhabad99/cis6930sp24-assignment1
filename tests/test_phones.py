import unittest
from censoror import censor_document

class TestPhones(unittest.TestCase):
    def test_censor_simple_phone(self):
        text = "Call me at 123-456-7890."
        censored_text = censor_document(text, {'PHONE_NUMBER'}, {'NAMES': 0, 'DATES': 0, 'ADDRESSES': 0, 'PHONE_NUMBERS': 0})
        self.assertEqual(censored_text, "Call me at ████████████.")

    def test_censor_formatted_phone(self):
        text = "My number is (123) 456-7890."
        censored_text = censor_document(text, {'PHONE_NUMBER'}, {'NAMES': 0, 'DATES': 0, 'ADDRESSES': 0, 'PHONE_NUMBERS': 0})
        self.assertEqual(censored_text, "My number is ██████████████.")

if __name__ == '__main__':
    unittest.main()
