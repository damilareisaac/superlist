from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    context: dict = {"to_do_item": request.POST.get("todo_input_text", "")}
    return render(
        request,
        "home.html",
        context,
    )
