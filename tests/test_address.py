import unittest
from censoror import censor_document

class TestAddress(unittest.TestCase):
    def test_censor_address(self):
        text = "My address is 123 Main St, Springfield, IL 62704."
        censored_text = censor_document(text, {'ADDRESS'}, {'NAMES': 0, 'DATES': 0, 'ADDRESSES': 0, 'PHONE_NUMBERS': 0})
        self.assertEqual(censored_text, "My address is ██████████████████████████████████.")

    def test_censor_address_with_punctuation(self):
        text = "Find us at 456 Elm St., Anytown, CA 90210."
        censored_text = censor_document(text, {'ADDRESS'}, {'NAMES': 0, 'DATES': 0, 'ADDRESSES': 0, 'PHONE_NUMBERS': 0})
        self.assertEqual(censored_text, "Find us at ██████████████████████████████.")

if __name__ == '__main__':
    unittest.main()
