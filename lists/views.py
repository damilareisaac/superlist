from django.http import HttpRequest, HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.html import escape
from lists.forms import EMPTY_ITEM_ERROR, ItemForm

from lists.models import Item, List


def home_page(request) -> HttpResponse:
    context = {"form": ItemForm()}
    return render(request, "home.html", context)


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == "POST":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            text_input = request.POST.get("text", "")
            Item.objects.create(text=text_input, list=list_)
            return redirect(list_)

    context = dict(
        list=list_,
        form=form,
    )
    return render(request, "list.html", context)


def new_list(request) -> HttpResponse:
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        text_input = request.POST.get("text", "")
        Item.objects.create(text=text_input, list=list_)
        return redirect(list_)

    context = dict(
        form=form,
    )
    return render(request, "home.html", context)
