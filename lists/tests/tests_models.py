from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List


class ListAndItemModelsTestCase(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "First dummy item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Second dummy item"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()

        self.assertEqual(saved_items.count(), 2)

        first_item = saved_items[0]
        second_item = saved_items[1]

        self.assertEqual(first_item.text, "First dummy item")
        self.assertEqual(first_item.list, list_)
        self.assertEqual(second_item.text, "Second dummy item")
        self.assertEqual(second_item.list, list_)

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f"/lists/{list_.id}/")

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="bla")
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text="bla")
            item.full_clean()

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="i1")
        item2 = Item.objects.create(list=list1, text="item 2")
        item3 = Item.objects.create(list=list1, text="3")
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_string_representation(self):
        item = Item(text="some text")
        self.assertEqual(str(item), "some text")

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())


class ItemModelTestCase(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, "")
