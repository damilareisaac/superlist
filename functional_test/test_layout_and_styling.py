from functional_test.base import FunctionalTestCase


class SmokeTestCase(FunctionalTestCase):
    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        self.send_to_do_item("testing")
        self.wait_for(lambda: self.check_row_in_list_table("1. testing"))

        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10,
        )
