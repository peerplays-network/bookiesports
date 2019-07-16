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

    def test_beatrice(self):
        beatrice = BookieSports("beatrice")
        self.assertEqual(beatrice.chain_id, "b3f7fe1e5ad0d2deca40a626a4404524f78e65c3a48137551c33ea4e7c365672")

    def test_charlie(self):
        charlie = BookieSports("charlie")
        self.assertEqual(charlie.chain_id, "*")
    
    def test_fred(self):
        fred = BookieSports("fred")
        self.assertEqual(fred.chain_id, "fb6ff714f8dfcf97eef01591fc938aa97755bf641aef711b3609a94578df9e5e")

    def test_list_chains(self):
        networks = BookieSports.list_chains()
        self.assertIn("alice", networks)
        self.assertIn("beatrice", networks)
        self.assertIn("charlie", networks)
        self.assertIn("fred", networks)

    def test_version(self):
        print()
        pprint(BookieSports.version())
        print()
