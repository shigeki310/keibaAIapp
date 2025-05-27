import unittest
from pathlib import Path
import sys
import os

# Dynamically add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "../src")
sys.path.append(src_path)

from scraping import scrape_kaisai_date, scrape_race_id_list, scrape_html_race

class TestScraping(unittest.TestCase):

    def test_scrape_kaisai_date(self):
        from_date = "2023-01"
        to_date = "2023-02"
        result = scrape_kaisai_date(from_date, to_date)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_scrape_race_id_list(self):
        kaisai_dates = ["20230105"]
        result = scrape_race_id_list(kaisai_dates)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_scrape_html_race(self):
        race_ids = ["202301010101"]
        save_dir = Path("../data/html/test")
        result = scrape_html_race(race_ids, save_dir)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        self.assertTrue(result[0].is_file())

if __name__ == "__main__":
    unittest.main()