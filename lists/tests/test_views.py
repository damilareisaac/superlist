from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.utils.html import escape
from django.urls import ResolverMatch, resolve
from lists.forms import (
    DUPLICATE_ITEM_ERROR,
    EMPTY_ITEM_ERROR,
    ExistingListItemForm,
    ItemForm,
)
from lists.views import home_page
from lists.models import Item, List


class SmokeTestCase(TestCase):
    def test_bad_maths(self) -> None:
        self.assertEqual(1 + 1, 2)


class HomePageTestCase(TestCase):
    def test_root_url_resolves_to_home_page_view(self) -> None:
        found: ResolverMatch = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response: HttpResponse = home_page(request)
        html: str = response.content.decode("utf-8")
        self.assertTrue(html.strip().startswith("<!Doctype>"))
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.strip().endswith("</html>"))

    def test_uses_home_template_using_client(self):
        response: HttpResponse = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class TestListView(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()

        response = self.client.get(
            f"/lists/{list_.id}/",
        )
        self.assertTemplateUsed(response, "list.html")

    def test_home_page_uses_item_form(self):
        response = self.client.get("/")
        self.assertIsInstance(response.context.get("form"), ItemForm)

    def test_display_all_items(self):
        list_: List = List.objects.create()
        Item.objects.create(text="First fake item", list=list_)
        Item.objects.create(text="Second fake item", list=list_)

        response: HttpResponse = self.client.get(f"/lists/{list_.id}/")

        self.assertContains(response, "First fake item")
        self.assertContains(response, "Second fake item")

    def test_display_only_items_for_that_list(self):
        list_: List = List.objects.create()
        Item.objects.create(text="First fake item", list=list_)
        Item.objects.create(text="Second fake item", list=list_)

        other_list: List = List.objects.create()
        Item.objects.create(text="Other List First fake item", list=other_list)
        Item.objects.create(text="Other List Second fake item", list=other_list)

        response: HttpResponse = self.client.get(f"/lists/{list_.id}/")

        self.assertContains(response, "First fake item")
        self.assertContains(response, "Second fake item")

        self.assertNotContains(response, "Other List First fake item")
        self.assertNotContains(response, "Other List Second fake item")

    def test_can_save_a_post_request(self):
        response: HttpResponse = self.client.post(
            "/lists/new", data={"text": "First Item"}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        list_ = List.objects.first()
        self.assertEqual(new_item.text, "First Item")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], f"/lists/{list_.id}/")

    def test_not_saving_empty_item(self):
        self.client.post("/lists/new")
        self.assertEqual(Item.objects.count(), 0)

    def test_redirects_after_post(self):
        response: HttpResponse = self.client.post(
            "/lists/new", data={"text": "New Item"}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_can_save_a_post_request_to_an_existing_list(self):
        List.objects.create()
        current_list = List.objects.create()

        self.client.post(
            f"/lists/{current_list.id}/",
            data={"text": "a new item for current list"},
        )
        self.assertEqual(Item.objects.count(), 1)
        added_item: Item | None = Item.objects.first()
        self.assertEqual(added_item.text, "a new item for current list")
        self.assertEqual(added_item.list, current_list)

    def test_redirect_to_list_view(self):
        List.objects.create()
        current_list: List = List.objects.create()

        response = self.client.post(
            f"/lists/{current_list.id}/",
            data={"text": "a new item for current list"},
        )
        self.assertRedirects(response, f"/lists/{current_list.id}/")

    def test_passes_correct_list_to_template(self):
        _: List = List.objects.create()
        current_list: List = List.objects.create()
        response: HttpResponse = self.client.post(f"/lists/{current_list.id}/")
        self.assertEqual(response.resolver_match.kwargs.get("list_id"), current_list.id)

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post("/lists/new", data={"todo_input_text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            f"/lists/{list_.id}/",
            data={"todo_input_text": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list.html")
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertIsInstance(response.context.get("form"), ItemForm)
        self.assertContains(response, 'name="text')

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(f"/lists/{list_.id}/", data={"text": ""})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list.html")

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context["form"], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="textey")
        response = self.client.post(f"/lists/{list1.id}/", data={"text": "textey"})

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, "list.html")
        self.assertEqual(Item.objects.all().count(), 1)
