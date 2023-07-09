from django.http import (
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import redirect, render

from lists.models import Item


def home_page(request) -> HttpResponse:
    return render(request, "home.html")


def view_list(request) -> HttpResponse:
    items = Item.objects.all()
    context = dict(items=items)
    return render(request, "list.html", context)


def new_list(request) -> HttpResponse:
    text_input = request.POST.get("todo_input_text", "")
    if text_input:
        Item.objects.create(text=text_input)
    return redirect("/lists/the-only-list-in-the-world/")
