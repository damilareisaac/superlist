import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 5


class FunctionalTestCase(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser: webdriver.Firefox = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def check_row_in_list_table(self, row_text) -> None:
        table = self.browser.find_element(
            By.ID,
            "to-do_items_list_table",
        )
        rows = table.find_elements(
            By.TAG_NAME,
            "tr",
        )
        self.assertIn(row_text, [row.text for row in rows])

    def send_to_do_item(self, item_text) -> None:
        to_do_input_box = self.get_item_input_box()
        to_do_input_box.send_keys(item_text)

        # When she hits enter, the page updates,
        # and now the page lists
        to_do_input_box.send_keys(Keys.ENTER)

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def get_item_input_box(self):
        return self.browser.find_element(By.ID, "id_text")
