import unittest
from bookiesports import BookieSports
from pprint import pprint


class Testcases(unittest.TestCase):

    def test_bookiesports(self):
        # Validation happens inside
        BookieSports()

    def test_alice(self):
        charlie = BookieSports("alice")
        self.assertEqual(charlie.chain_id, "6b6b5f0ce7a36d323768e534f3edb41c6d6332a541a95725b98e28d140850134")

    def test_baxter(self):
        charlie = BookieSports("baxter")
        self.assertEqual(charlie.chain_id, "be6b79295e728406cbb7494bcb626e62ad278fa4018699cf8f75739f4c1a81fd")

    def test_charlie(self):
        charlie = BookieSports("charlie")
        self.assertEqual(charlie.chain_id, "*")

    def test_list_networks(self):
        networks = BookieSports.list_networks()
        self.assertIn("alice", networks)
        self.assertIn("baxter", networks)
        self.assertIn("charlie", networks)

    def test_version(self):
        print()
        pprint(BookieSports.version())
        print()
