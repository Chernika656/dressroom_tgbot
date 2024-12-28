# dresswebapp/views.py
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>Приветствуем в DressWebApp!</h1>")  # Или render(...) для шаблона
