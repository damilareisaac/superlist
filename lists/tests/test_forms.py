from django.test import TestCase
from lists.forms import EMPTY_ITEM_ERROR, ItemForm
from lists.models import Item, List


class ItemFormTestCase(TestCase):
    def test_form_renders_item_text_input(self):
        form = ItemForm()

    def test_form_item_input_has_placeholder_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors.get("text"),
            [EMPTY_ITEM_ERROR],
        )

    def test_form_save_handles_saving_to_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={"text": "New Item"})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, "New Item")
        self.assertEqual(new_item.list, list_)
