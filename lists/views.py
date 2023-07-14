from django.http import HttpRequest, HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.html import escape

from lists.models import Item, List


def home_page(request) -> HttpResponse:
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    if request.method == "POST":
        text_input = request.POST.get("todo_input_text", "")
        Item.objects.create(text=text_input, list=list_)
        return redirect(f"/lists/{list_.id}/")
    context = dict(list=list_)
    return render(request, "list.html", context)


def new_list(request) -> HttpResponse:
    list_ = List.objects.create()
    text_input = request.POST.get("todo_input_text", "")
    item = Item.objects.create(text=text_input, list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = escape("You can't have an empty list item")
        context = dict(error=error)
        return render(request, "home.html", context)
    return redirect(f"/lists/{list_.id}/")
