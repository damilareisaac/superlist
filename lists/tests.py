from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.urls import ResolverMatch, resolve
from lists.views import home_page


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

    def test_can_save_a_post_request(self):
        response: HttpResponse = self.client.post(
            "/", data={"todo_input_text": "First Item"}
        )
        self.assertIn("First Item", response.content.decode("utf-8"))
        self.assertTemplateUsed(response, "home.html")
