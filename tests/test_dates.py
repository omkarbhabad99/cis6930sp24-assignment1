import unittest
from censoror import censor_document

class TestDates(unittest.TestCase):
    def test_censor_simple_date(self):
        text = "The meeting is on 4/9/2025."
        # Modified line below
        censored_text = censor_document(text, {'DATE'}, {'NAMES': 0, 'DATES': 0, 'ADDRESSES': 0, 'PHONE_NUMBERS': 0})
        self.assertEqual(censored_text, "The meeting is on ████████.")

    def test_censor_full_date(self):
        text = "We will reconvene on April 9th, 2025."
        # Modified line below
        censored_text = censor_document(text, {'DATE'}, {'NAMES': 0, 'DATES': 0, 'ADDRESSES': 0, 'PHONE_NUMBERS': 0})
        self.assertEqual(censored_text, "We will reconvene on ███████████████.")

if __name__ == '__main__':
    unittest.main()
