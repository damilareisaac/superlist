from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.urls import ResolverMatch, resolve
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
            "/lists/new", data={"todo_input_text": "First Item"}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        list_ = List.objects.first()
        self.assertEqual(new_item.text, "First Item")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], f"/lists/{list_.id}/")

    # def test_not_saving_empty_item(self):
    #     self.client.post("/lists/new")
    #     self.assertEqual(Item.objects.count(), 0)

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
            f"/lists/{current_list.id}/add_item",
            data={"todo_input_text": "a new item for current list"},
        )

        self.assertEqual(Item.objects.count(), 1)
        added_item: Item | None = Item.objects.first()
        self.assertEqual(added_item.text, "a new item for current list")
        self.assertEqual(added_item.list, current_list)

    def test_redirect_to_list_view(self):
        List.objects.create()
        current_list: List = List.objects.create()

        response = self.client.post(
            f"/lists/{current_list.id}/add_item",
            data={"todo_input_text": "a new item for current list"},
        )
        self.assertRedirects(response, f"/lists/{current_list.id}/")

    def test_passes_correct_list_to_template(self):
        _: List = List.objects.create()
        current_list: List = List.objects.create()
        response = self.client.post(f"/lists/{current_list.id}/")
        self.assertEqual(response.context.get("list"), current_list)
