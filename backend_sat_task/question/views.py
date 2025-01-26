from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def create_question(request):
    return render(request, "create_question.html")
