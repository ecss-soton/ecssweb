import unittest
from selenium import webdriver

class HomepageTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_attributes(self):
        driver = self.driver
        driver.get("http://localhost:8000")
        self.assertIn("ECSS - University of Southampton Electronics and Computer Science Society", driver.title)

    def tearDown(self):
        self.driver.close()
