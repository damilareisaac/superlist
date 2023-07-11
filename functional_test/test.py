import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 5


class CustomLiveServerTestCase(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser: webdriver.Firefox = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def check_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, "to-do_items_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row.text for row in rows])

    def wait_for_low_in_list_table(self, row_text: str):
        start_time = time.time()
        while True:
            try:
                self.check_row_in_list_table(row_text)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    def send_to_do_item(self, item_text):
        to_do_input_box = self.browser.find_element(
            By.ID,
            "todo_input_text",
        )
        to_do_input_box.send_keys(item_text)

        # When she hits enter, the page updates, and now the page lists
        to_do_input_box.send_keys(Keys.ENTER)


class SmokeTestCase(CustomLiveServerTestCase):
    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        self.send_to_do_item("testing")
        self.wait_for_low_in_list_table("1. testing")

        inputbox = self.browser.find_element(By.ID, "todo_input_text")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10,
        )


class TestFunctionalityTestCase(CustomLiveServerTestCase):
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        #   to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)

        # she notices the page title and header mentioned to-do lists
        header_text: str = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Start a new To-Do list", header_text)

        # She is invited to enter a to-do item straight away
        to_do_input_box = self.browser.find_element(By.ID, "todo_input_text")
        self.assertEqual(
            to_do_input_box.get_attribute("placeholder"), "Enter a to-do item"
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        self.send_to_do_item("Buy peacock feathers")

        self.wait_for_low_in_list_table("1. Buy peacock feathers")
        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)

        self.send_to_do_item("Use peacock feathers to make a fly")

    # def test_can_start_a_list_with_one_user(self):
    #     # Edith has heard about a cool new online to-do app. She goes
    #     # The page updates again, and now shows both items on her list

    #     self.wait_for_low_in_list_table("1. Buy peacock feathers")
    #     self.wait_for_low_in_list_table("2. Use peacock feathers to make a fly")

    def test_multiple_users_can_add_items_to_lists_at_different_url(self):
        # Edith start a new list

        self.browser.get(self.live_server_url)
        self.send_to_do_item("Buy peacock feathers")
        self.wait_for_low_in_list_table("1. Buy peacock feathers")

        # She notices that her list has a unique URL

        edith_url = self.browser.current_url
        self.assertRegex(edith_url, "lists/.+")

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("Use peacock feathers to make a fly", page_text)

        # Francis started a new list by entering an item

        self.send_to_do_item("Buy milk")
        self.wait_for_low_in_list_table("1. Buy milk")

        francis_url = self.browser.current_url
        self.assertRegex(francis_url, "lists/.+")

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

        # Satisfied, they both go back to sleep
