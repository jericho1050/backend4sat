import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_pic = models.ImageField(
        upload_to="profile_pictures/",
        height_field=None,
        width_field=None,
        null=True,
        blank=True,
    )
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]
    question = models.TextField()
    solution = models.TextField()
    correct_answer = models.CharField(max_length=255)
    image_url = models.URLField(blank=True, null=True)  # noqa: DJ001
    tags = models.ManyToManyField("Tag", related_name="questions", blank=True)
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default="easy",
    )

    def __str__(self):
        return self.question[:50]


class Option(models.Model):
    question = models.ForeignKey(
        "Question",
        related_name="options",
        on_delete=models.CASCADE,
    )
    option_text = models.CharField(max_length=255)

    def __str__(self):
        return self.option_text


class SolutionStep(models.Model):
    question = models.ForeignKey(
        Question,
        related_name="steps",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    result = models.TextField()
    image_url = models.URLField(blank=True, null=True)  # noqa: DJ001
    step_number = models.PositiveIntegerField()

    class Meta:
        ordering = ["step_number"]

    def __str__(self):
        return f"{self.title} - {self.question}"
