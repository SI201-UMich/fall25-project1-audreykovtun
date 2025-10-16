import unittest
from project1 import get_bill_depths
import csv
import os

from project1 import get_penguins

class TestGetPenguins(unittest.TestCase):

    def setUp(self):
        """Create test CSV files in the same directory as project1.py."""
        self.module_dir = os.path.dirname(os.path.abspath(__import__("project1").__file__))
        self.test_file = os.path.join(self.module_dir, "test_project1.csv")

        print("DEBUG: test file created at →", self.test_file)


        with open(self.test_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["penguin_number", "bill_length_mm", "bill_depth_mm"])
            writer.writerow(["1", "39.1", "18.7"])
            writer.writerow(["2", "39.5", "17.4"])

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    # ---- General Tests ----
    def test_basic_structure(self):
        result = get_penguins(self.test_file)
        self.assertIn("bill_length_mm", result)
        self.assertIn("bill_depth_mm", result)

    def test_values_are_floats(self):
        result = get_penguins(self.test_file)
        self.assertIsInstance(result["bill_length_mm"]["1"], float)
        self.assertEqual(result["bill_depth_mm"]["2"], 17.4)

    # ---- Edge Case Tests ----
    def test_empty_file(self):
        empty_file = os.path.join(self.module_dir, "empty_penguins.csv")
        with open(empty_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["penguin_number", "bill_length_mm"])
        result = get_penguins(empty_file)
        self.assertEqual(result, {})
        os.remove(empty_file)

    def test_non_numeric_values(self):
        non_numeric_file = os.path.join(self.module_dir, "non_numeric_penguins.csv")
        with open(non_numeric_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["penguin_number", "bill_length_mm"])
            writer.writerow(["1", "N/A"])
        result = get_penguins(non_numeric_file)
        self.assertEqual(result["bill_length_mm"]["1"], "N/A")
        os.remove(non_numeric_file)

if __name__ == "__main__":
    unittest.main()


from project1 import get_bill_depths


class TestGetBillDepths(unittest.TestCase):

    # ---- General Tests ----
    def test_multiple_species(self):
        """Test that bill depths are collected correctly across species."""
        penguin_dict = {
            "Adelie": {1: {"bill_depth_mm": "18.4"}, 2: {"bill_depth_mm": "17.9"}},
            "Chinstrap": {1: {"bill_depth_mm": "19.3"}}
        }
        expected = [18.4, 17.9, 19.3]
        self.assertEqual(get_bill_depths(penguin_dict), expected)

    def test_single_species_single_penguin(self):
        """Test one species with one penguin."""
        penguin_dict = {"Gentoo": {1: {"bill_depth_mm": "15.2"}}}
        expected = [15.2]
        self.assertEqual(get_bill_depths(penguin_dict), expected)

    # ---- Edge Case Tests ----
    def test_missing_values(self):
        """Test that missing or blank bill depths are ignored."""
        penguin_dict = {
            "Adelie": {
                1: {"bill_depth_mm": ""},
                2: {"bill_depth_mm": None},
                3: {"bill_depth_mm": "NA"},
                4: {"bill_depth_mm": "17.1"},
            }
        }
        expected = [17.1]
        self.assertEqual(get_bill_depths(penguin_dict), expected)

    def test_non_numeric_values(self):
        """Test that non-numeric bill depths are skipped safely."""
        penguin_dict = {
            "Adelie": {
                1: {"bill_depth_mm": "abc"},
                2: {"bill_depth_mm": "18.0"}
            }
        }
        expected = [18.0]
        self.assertEqual(get_bill_depths(penguin_dict), expected)

if __name__ == "__main__":
    unittest.main()

from project1 import get_average_bill_depths

class TestGetAverageBillDepths(unittest.TestCase):

    # ---- General Tests ----
    def test_multiple_species(self):
        """Test average calculation across multiple species."""
        penguin_dict = {
            "Adelie": {
                1: {"bill_depth_mm": 18.4},
                2: {"bill_depth_mm": 17.6},
                3: {"bill_depth_mm": 18.0}
            },
            "Chinstrap": {
                1: {"bill_depth_mm": 19.3},
                2: {"bill_depth_mm": 20.1}
            }
        }
        result = get_average_bill_depths(penguin_dict)
        self.assertAlmostEqual(result["Adelie"], (18.4 + 17.6 + 18.0) / 3)
        self.assertAlmostEqual(result["Chinstrap"], (19.3 + 20.1) / 2)

    def test_single_species_single_penguin(self):
        """Test average when there is only one penguin in a species."""
        penguin_dict = {"Gentoo": {1: {"bill_depth_mm": 15.2}}}
        result = get_average_bill_depths(penguin_dict)
        self.assertEqual(result["Gentoo"], 15.2)

    # ---- Edge Case Tests ----
    def test_missing_bill_depths(self):
        """Test species with missing bill_depth_mm values."""
        penguin_dict = {
            "Adelie": {1: {"bill_depth_mm": None}, 2: {}},
            "Chinstrap": {1: {"bill_depth_mm": 19.0}}
        }
        result = get_average_bill_depths(penguin_dict)
        self.assertIsNone(result["Adelie"])
        self.assertEqual(result["Chinstrap"], 19.0)

    def test_non_numeric_values(self):
        """Test that non-numeric values are ignored."""
        penguin_dict = {
            "Adelie": {
                1: {"bill_depth_mm": "abc"},
                2: {"bill_depth_mm": 18.0}
            }
        }
        result = get_average_bill_depths(penguin_dict)
        self.assertEqual(result["Adelie"], 18.0)

if __name__ == "__main__":
    unittest.main()

from project1 import locate_above_avg

class TestLocateAboveAvg(unittest.TestCase):

    # ---- General Tests ----
    def test_mixed_species_above_avg(self):
        """Test that penguins above their species average are correctly identified."""
        bill_depths = [
            {"species": "Adelie", "bill_depth_mm": 18.4, "body_mass_g": 3700},
            {"species": "Adelie", "bill_depth_mm": 17.2, "body_mass_g": 3600},
            {"species": "Chinstrap", "bill_depth_mm": 20.0, "body_mass_g": 3800},
        ]
        averages = {"Adelie": 17.8, "Chinstrap": 19.0}

        result = locate_above_avg(bill_depths, averages)
        self.assertEqual(sorted(result), sorted([3700, 3800]))

    def test_all_below_average(self):
        """Return empty list when no penguins exceed the average."""
        bill_depths = [
            {"species": "Adelie", "bill_depth_mm": 16.9, "body_mass_g": 3500},
            {"species": "Chinstrap", "bill_depth_mm": 18.5, "body_mass_g": 3750},
        ]
        averages = {"Adelie": 17.5, "Chinstrap": 19.0}

        result = locate_above_avg(bill_depths, averages)
        self.assertEqual(result, [])

    # ---- Edge Case Tests ----
    def test_missing_species_mean(self):
        """Penguins with missing species mean should be ignored."""
        bill_depths = [
            {"species": "Unknown", "bill_depth_mm": 20.0, "body_mass_g": 4000},
            {"species": "Adelie", "bill_depth_mm": 18.1, "body_mass_g": 3700},
        ]
        averages = {"Adelie": 17.9}

        result = locate_above_avg(bill_depths, averages)
        self.assertEqual(result, [3700])

    def test_invalid_data_types(self):
        """Non-numeric bill depths or masses should be skipped."""
        bill_depths = [
            {"species": "Adelie", "bill_depth_mm": "18.4", "body_mass_g": 3700},
            {"species": "Adelie", "bill_depth_mm": 18.6, "body_mass_g": "3800"},
            {"species": "Adelie", "bill_depth_mm": 19.0, "body_mass_g": 4000},
        ]
        averages = {"Adelie": 18.5}

        result = locate_above_avg(bill_depths, averages)
        self.assertEqual(result, [4000])

if __name__ == "__main__":
    unittest.main()

from project1 import finalize_report

class TestFinalizeReport(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_penguin_report.txt"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    # ---- General Tests ----
    def test_normal_report(self):
        """Test that a well-formed report is written correctly."""
        averages = {"Adelie": 18.15, "Chinstrap": 19.3}
        masses = [3700, 3800]

        finalize_report(averages, masses, filename=self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

        with open(self.test_file, "r") as f:
            content = f.read()

        self.assertIn("Adelie: 18.15 mm", content)
        self.assertIn("Chinstrap: 19.30 mm", content)
        self.assertIn("3700g", content)
        self.assertIn("3800g", content)

    def test_empty_masses_list(self):
        """Test that report still generates if no above-average masses."""
        averages = {"Gentoo": 17.9}
        masses = []

        finalize_report(averages, masses, filename=self.test_file)

        with open(self.test_file, "r") as f:
            content = f.read()

        self.assertIn("Gentoo: 17.90 mm", content)
        self.assertIn("None", content)

    # ---- Edge Case Tests ----
    def test_empty_means_dict(self):
        """Test that function handles empty means dictionary gracefully."""
        averages = {}
        masses = [3500, 3600]

        finalize_report(averages, masses, filename=self.test_file)

        with open(self.test_file, "r") as f:
            content = f.read()

        self.assertIn("No data available.", content)
        self.assertIn("3500g", content)

    def test_no_data_at_all(self):
        """Test report creation when both inputs are empty."""
        averages = {}
        masses = []

        finalize_report(averages, masses, filename=self.test_file)

        with open(self.test_file, "r") as f:
            content = f.read()

        self.assertIn("No data available.", content)
        self.assertIn("None", content)

if __name__ == "__main__":
    unittest.main()