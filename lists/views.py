from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item


def home_page(request) -> HttpResponse:
    if request.method == "POST":
        item_input = request.POST.get("todo_input_text", "")
        if item_input.strip():
            Item.objects.create(text=item_input)
            return redirect("/")
    items = Item.objects.all()
    context = dict(items=items)
    return render(request, "home.html", context)
