from selenium import webdriver
from selenium.webdriver.common.by import By
from functional_test.base import FunctionalTestCase


class TestSimpleListCreationTestCase(FunctionalTestCase):
    def test_multiple_users_can_add_items_to_lists_at_different_url(self):
        # Edith start a new list

        self.browser.get(self.live_server_url)
        self.send_to_do_item("Buy peacock feathers")
        self.wait_for(lambda: self.check_row_in_list_table("1. Buy peacock feathers"))

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
        self.wait_for(lambda: self.check_row_in_list_table("1. Buy milk"))

        francis_url = self.browser.current_url
        self.assertRegex(francis_url, "lists/.+")

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

        # Satisfied, they both go back to sleep
