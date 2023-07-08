from django.urls import path
import lists.views as views


urlpatterns = [
    path("", views.home_page, name="list_home"),
]
