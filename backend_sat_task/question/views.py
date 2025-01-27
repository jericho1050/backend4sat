from django.shortcuts import render

from .models import Question


def index(request):
    return render(request, "index.html")


def create_question(request):
    return render(request, "create_question.html")


def check_answer(request):
    question_id = request.POST.get("question_id")
    answer = request.POST.get("answer")

    question = Question.objects.get(id=question_id)
    is_correct = answer == question.correct_answer

    return render(
        request,
        "explanation.html",
        {"question": question, "is_correct": is_correct},
    )
