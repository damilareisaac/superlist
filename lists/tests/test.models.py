from django.test import TestCase
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
