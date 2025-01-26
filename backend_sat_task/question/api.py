from typing import List  # noqa: UP035

import boto3
from django.conf import settings
from django.shortcuts import get_object_or_404
from ninja import File
from ninja import NinjaAPI
from ninja.files import UploadedFile
from ninja.pagination import paginate
from ninja.throttling import AnonRateThrottle
from ninja.throttling import AuthRateThrottle

from .auth import ApiKey
from .models import Option
from .models import Question
from .models import SolutionStep
from .models import Tag
from .schemas import QuestionIn
from .schemas import QuestionOut
from .schemas import QuestionPatchSchema

api = NinjaAPI(
    version="v0",
    throttle=[AuthRateThrottle("50/s"), AnonRateThrottle("10/s")],
)

api_key = ApiKey()


@api.get(
    "/questions",
    by_alias=True,
    response=List[QuestionOut],  # noqa: UP006
    url_name="question_list",
)  # noqa: E501, RUF100, UP006
@paginate
def get_questions(request):
    questions = Question.objects.prefetch_related("options", "steps", "tags").all()
    return [
        {
            "Id": q.id,
            "Question": q.question,
            "Solution": q.solution,
            "CorrectAnswer": q.correct_answer,
            "Options": [opt.option_text for opt in q.options.all()],
            "Steps": q.steps.all(),
            "ImageUrl": q.image_url,
            "Difficulty": q.difficulty,
            "Tags": q.tags.all(),
        }
        for q in questions
    ]


@api.get(
    "/question/{question_id}",
    by_alias=True,
    response=QuestionOut,
    url_name="question_retrieve",
)
def get_question(request, question_id: int):
    question = get_object_or_404(Question, id=question_id)
    return {
        "Id": question.id,
        "Question": question.question,
        "Solution": question.solution,
        "CorrectAnswer": question.correct_answer,
        "Options": [opt.option_text for opt in question.options.all()],
        "steps": question.steps.all(),
        "ImageUrl": question.image_url,
        "Difficulty": question.difficulty,
        "Tags": question.tags.all(),
    }


@api.post(
    "/questions",
    auth=api_key,
    by_alias=True,
    response=QuestionOut,
    url_name="question_create",
)
def create_question(request, payload: QuestionIn):
    # Extract nested data
    data = payload.dict()
    options_data = data.pop("options", [])
    steps_data = data.pop("steps", [])
    tags_data = data.pop("tags", [])  # Extract tags

    # Create main question
    question = Question.objects.create(**data)

    # Create or get tags and link them
    for tag_data in tags_data:
        tag, _ = Tag.objects.get_or_create(
            name=tag_data["name"],
            defaults={"slug": tag_data["slug"]},
        )
        question.tags.add(tag)

    # Create related options
    for option in options_data:
        Option.objects.create(question=question, option_text=option)

    # Create related steps
    for index, step in enumerate(steps_data, start=1):
        SolutionStep.objects.create(
            question=question,
            title=step["title"],
            result=step["result"],
            image_url=step.get("image_url"),
            step_number=index,
        )

    return {
        "id": question.id,
        "question": question.question,
        "solution": question.solution,
        "correct_answer": question.correct_answer,
        "options": [opt.option_text for opt in question.options.all()],
        "steps": question.steps.all(),
        "image_url": question.image_url,
        "difficulty": question.difficulty,
        "tags": [{"name": tag.name, "slug": tag.slug} for tag in question.tags.all()],
    }


@api.patch(
    "/question/{question_id}",
    auth=api_key,
    by_alias=True,
    url_name="question_update",
    response=QuestionOut,
)
def patch_question(request, question_id: int, payload: QuestionPatchSchema):
    question = get_object_or_404(Question, id=question_id)
    data = payload.dict(exclude_unset=True)  # Only get set values

    # Handle nested fields if provided
    options_data = data.pop("options", None)
    steps_data = data.pop("steps", None)
    tags_data = data.pop("tags", None)

    # Update main fields if provided
    for field, value in data.items():
        setattr(question, field, value)
    question.save()

    # Update relations only if provided
    if tags_data is not None:
        # Clear existing tags
        question.tags.clear()
        # Create or get tags and add them
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(
                name=tag_data["name"],
                defaults={"slug": tag_data["slug"]},
            )
            question.tags.add(tag)

    if options_data is not None:
        question.options.all().delete()
        for option_text in options_data:
            Option.objects.create(question=question, option_text=option_text)

    if steps_data is not None:
        question.steps.all().delete()
        for index, step_data in enumerate(steps_data, start=1):
            SolutionStep.objects.create(
                question=question,
                title=step_data["title"],
                result=step_data["result"],
                image_url=step_data.get("image_url"),
                step_number=index,
            )

    return get_question(request, question_id)


@api.delete("/question/{question_id}", auth=api_key, url_name="question_delete")
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    return {"sucess": True}


@api.post("/upload-image", auth=api_key, url_name="image_upload")
def upload_image(request, file: UploadedFile = File(...)):  # noqa: B008
    """Upload image to S3 and return public URL"""
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    # Upload to S3
    file_name = f"images/{file.name}"
    s3_client.upload_fileobj(
        file.file,
        settings.AWS_STORAGE_BUCKET_NAME,
        file_name,
    )

    # Generate public URL
    url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_name}"

    return {"url": url}


@api.get("/validate-key", auth=api_key, include_in_schema=False)
def validate_api_key(request):
    """Endpoint to validate API key"""
    return {"valid": True}
