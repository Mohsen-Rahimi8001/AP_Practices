import unittest
from medad_rangi import MedadRangi
from unittest.mock import patch
import datetime as dt

class TestMedadRangi(unittest.TestCase):
    def test_init(self):
        MedadRangi("item1", 1000, 10, 'IR', "UnkownCompany")
        self.assertRaises(ValueError, MedadRangi, "", 1000, 10, 'IR', "UnkownCompany")
        self.assertRaises(TypeError, MedadRangi, 123, 1000, 10, 'IR', "UnkownCompany")
        
        self.assertRaises(ValueError, MedadRangi, "item1", 1000, 10, 'IR', "")
        self.assertRaises(TypeError, MedadRangi, "item1", 1000, 10, 'IR', 1.2)
        
        self.assertRaises(ValueError, MedadRangi, "item1", 1000, 10, '', "UnkownCompany")
        self.assertRaises(TypeError, MedadRangi, "item1", 1000, 10, [], "UnkownCompany")

        self.assertRaises(ValueError, MedadRangi, "item1", 1000, -1, 'IR', "UnkownCompany")
        self.assertRaises(TypeError, MedadRangi, "item1", 1000, '10', 'IR', "UnkownCompany")
        
        self.assertRaises(ValueError, MedadRangi, "item1", -0.5, 10, 'IR', "UnkownCompany")
        self.assertRaises(TypeError, MedadRangi, "item1", [1000], 10, 'IR', "UnkownCompany")

    def test_welcome(self):
        # when the medad_rangi uses other datetime functions besides dt.datetime.now() they will be forwarded to the original wrapped datetime module.
        with patch("medad_rangi.dt", wraps=dt) as mocked: 
            mocked.datetime.now.return_value = dt.datetime(1, 1, 1, 12)
            self.assertEqual(MedadRangi.welcome(), "Good morning!!!")

            mocked.datetime.now.return_value = dt.datetime(1, 1, 1, 6)
            self.assertEqual(MedadRangi.welcome(), "Good morning!!!")

            mocked.datetime.now.return_value = dt.datetime(1, 1, 1, 18)
            self.assertEqual(MedadRangi.welcome(), "Good evening!!!")

            mocked.datetime.now.return_value = dt.datetime(1, 1, 1, 5)
            self.assertEqual(MedadRangi.welcome(), "The shop is closed!!!")

    def test_add_item(self):
        item = MedadRangi("item2", 523.52, 5, "USA", "Unknown")
        MedadRangi.add_item("item2", 523.52, 5, "USA", "Unknown")
        self.assertListEqual(MedadRangi.items, [item])

    def test_final_price(self):
        item = MedadRangi("item2", 1000, 5, "USA", "Unknown")
        self.assertEqual(item.final_price(), item.price * 0.9)

    def test_calculate_distance(self):
        dest_loc = (0, 0)
        expected_distance = 6633.083323095385
        self.assertAlmostEqual(expected_distance, MedadRangi.calculate_distance(dest_loc), places=5)

    def test_load_csv(self):
        MedadRangi.items = []
        item1 = MedadRangi("item1", 523.52, 5, "USA", "Unknown")
        item2 = MedadRangi("item2", 523.52, 5, "IR", "Unknown")
        item3 = MedadRangi("item3", 523.52, 5, "UK", "Unknown")
        item4 = MedadRangi("item4", 523.52, 5, "GER", "Unknown")
        item5 = MedadRangi("item5", 523.52, 5, "IR", "Unknown")
        MedadRangi.loat_csv(r".\Medad_Rangi\test.csv")
        self.assertListEqual([item1, item2, item3, item4, item5], MedadRangi.items)

if __name__ == '__main__':
    unittest.main(verbosity=2)
