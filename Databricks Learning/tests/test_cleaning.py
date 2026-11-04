import unittest
from retail_de.cleaning import normalize_name


class NameContractTests(unittest.TestCase):
    def test_name_contract(self):
        cases = [(None, None), ("", None), (" \t ", None),
                 ("  Alice \t Smith \n", "ALICE SMITH"),
                 ("bob", "BOB"), ("O'Neil", "O'NEIL")]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(normalize_name(raw), expected)

    def test_rejects_non_text(self):
        with self.assertRaises(TypeError):
            normalize_name(123)

    def test_normalization_is_idempotent(self):
        for value in [None, " alice  smith ", "", "bob"]:
            once = normalize_name(value)
            self.assertEqual(normalize_name(once), once)


if __name__ == "__main__":
    unittest.main()
