from django.urls import path

from .views import create_question
from .views import index

urlpatterns = [
    path("", index, name="index"),
    path("create-question", create_question, name="create_question"),
]
