from django.urls import path
import lists.views as views


urlpatterns = [
    path("", views.home_page, name="list_home"),
    path("lists/new", views.new_list, name="new_list"),
    path(
        "lists/the-only-list-in-the-world/",
        views.view_list,
        name="view_list",
    ),
]
