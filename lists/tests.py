from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.urls import ResolverMatch, resolve
from lists.views import home_page

from lists.models import Item


class ItemModelTestCase(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "First dummy item"
        first_item.save()
        second_item = Item()
        second_item.text = "Second dummy item"
        second_item.save()

        items = Item.objects.all()

        first_item = items[0]
        second_item = items[1]

        self.assertEqual(first_item.text, "First dummy item")
        self.assertEqual(second_item.text, "Second dummy item")
        self.assertEqual(items.count(), 2)


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
        self.assertTrue(html.strip().startswith("<html>"))
        self.assertIn("<title>To-Do</title>", html)
        self.assertTrue(html.strip().endswith("</html>"))

    def test_uses_home_template_using_client(self):
        response: HttpResponse = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class TestListView(TestCase):
    def test_uses_list_template(self):
        response = self.client.get(
            "/lists/the-only-list-in-the-world/",
        )
        self.assertTemplateUsed(response, "list.html")

    def test_display_all_items(self):
        Item.objects.create(text="First fake item")
        Item.objects.create(text="Second fake item")
        response: HttpResponse = self.client.get(
            "/lists/the-only-list-in-the-world/",
        )

        self.assertContains(response, "First fake item")
        self.assertContains(response, "Second fake item")

    def test_can_save_a_post_request(self):
        response: HttpResponse = self.client.post(
            "/lists/new", data={"todo_input_text": "First Item"}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "First Item")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"],
            "/lists/the-only-list-in-the-world/",
        )

    def test_not_saving_empty_item(self):
        self.client.post("/lists/new")
        self.assertEqual(Item.objects.count(), 0)

    def test_redirects_after_post(self):
        response: HttpResponse = self.client.post(
            "/lists/new", data={"text": "New Item"}
        )
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(
        #     response["location"],
        #     "lists/the-only-list-in-the-world/",
        # )
        self.assertRedirects(
            response,
            "/lists/the-only-list-in-the-world/",
        )
