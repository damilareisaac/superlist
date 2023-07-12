from selenium.webdriver.common.by import By
from functional_test.base import FunctionalTestCase


class SmokeTestCase(FunctionalTestCase):
    # @skip("saving time")
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
