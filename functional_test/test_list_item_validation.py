from selenium.webdriver.common.by import By
from functional_test.base import FunctionalTestCase


class TestListItemValidation(FunctionalTestCase):
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        #   to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do lists", self.browser.title)

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