import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from backend_sat_task.question.models import Option
from backend_sat_task.question.models import Question
from backend_sat_task.question.models import SolutionStep
from backend_sat_task.question.models import Tag


class Command(BaseCommand):
    help = "Create questions from JSON file"

    def handle(self, *args, **kwargs):
        # set the path to the datafile
        datafile = settings.APPS_DIR / "data" / "questions.json"
        assert datafile.exists()

        # load the datafile
        with open(datafile) as f:  # noqa: PTH123
            data = json.load(f)

        # Logic here for serializing json data
        for q in data:
            # Handle nested fields if provided
            options_data = q.pop("options", [])
            steps_data = q.pop("steps", [])
            tags_data = q.pop("tags", [])
            question = Question.objects.create(**q)

            # Handle tags with proper slug generation
            if tags_data:
                tag_objects = []
                for tag_name in tags_data:
                    tag, _ = Tag.objects.get_or_create(
                        name=tag_name, defaults={"slug": slugify(tag_name)}
                    )
                    tag_objects.append(tag)
                question.tags.set(tag_objects)
            for option_text in options_data:
                Option.objects.create(question=question, option_text=option_text)
            for i, step in enumerate(steps_data, start=1):
                SolutionStep.objects.create(question=question, step_number=i, **step)
