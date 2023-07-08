from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser: webdriver.Firefox = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def check_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, "to-do_items-list-table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        #   to check out its homepage
        self.browser.get("http://mysite.com:8000/")

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)

        # she notices the page title and header mentioned to-do lists
        header_text: str = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away
        to_do_input_box = self.browser.find_element(
            By.ID,
            "todo_input_text",
        )
        self.assertEqual(
            to_do_input_box.get_attribute("placeholder"), "Enter a to-do item"
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)

        to_do_input_box.send_keys("Buy peacock feathers")

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list

        to_do_input_box.send_keys(Keys.ENTER)

        time.sleep(2)
        self.check_row_in_list_table("1: Buy peacock feathers")
        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)

        time.sleep(1)
        to_do_input_box.send_keys("Use peacock feathers to make a fly")

        to_do_input_box.send_keys(Keys.ENTER)

        time.sleep(1)
        self.check_row_in_list_table("1: Buy peacock feathers")
        self.check_row_in_list_table("2. Use peacock feathers to make a fly")

        self.fail("Finish the test!")


# Edith wonders whether the site will remember her list. Then she sees
# that the site has generated a unique URL for her -- there is some
# explanatory text to that effect.

# She visits that URL - her to-do list is still there.

# Satisfied, she goes back to sleep

if __name__ == "__main__":
    unittest.main()
