from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from lists.forms import ExistingListItemForm, ItemForm

from lists.models import Item, List


def home_page(request) -> HttpResponse:
    context = {"form": ItemForm()}
    return render(request, "home.html", context)


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)

    return render(request, "list.html", dict(list=list_, form=form))


def new_list(request) -> HttpResponse:
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    return render(request, "home.html", dict(form=form))
