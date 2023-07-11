from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import redirect, render

from lists.models import Item, List


def home_page(request) -> HttpResponse:
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    context = dict(items=items, list=list_)
    return render(request, "list.html", context)


def new_list(request) -> HttpResponse:
    list_ = List.objects.create()
    text_input = request.POST.get("todo_input_text", "")
    Item.objects.create(text=text_input, list=list_)
    # if text_input:
    #     Item.objects.create(text=text_input, list=list_)
    return redirect(f"/lists/{list_.id}/")


def add_item(request, list_id: int):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["todo_input_text"], list=list_)
    return redirect(f"/lists/{list_.id}/")
