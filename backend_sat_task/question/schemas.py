from enum import Enum  # noqa: I001
from typing import List, Optional  # noqa: UP035
from ninja import ModelSchema, Schema
from pydantic import alias_generators

from .models import SolutionStep

# https://django-ninja.dev/guides/response/config-pydantic/
# Keep in mind that when you want modify output for field names (like cammel case)
# - you need to set as well populate_by_name and by_alias


class DifficultyEnum(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class Tag(Schema):
    name: str
    slug: str

    class Config:
        alias_generator = alias_generators.to_pascal
        populate_by_name = True  # needed if invoking to_pascal


class SolutionStepSchema(ModelSchema):
    class Config:
        model = SolutionStep
        model_fields = ["title", "result", "image_url", "step_number"]
        alias_generator = alias_generators.to_pascal
        populate_by_name = True  # needed if invoking to_pascal

class QuestionIn(Schema):
    question: str
    solution: str
    correct_answer: str
    options: List[str]  # noqa: UP006
    steps: List[SolutionStepSchema]  # noqa: UP006
    image_url: Optional[str] = None  # noqa: UP007
    difficulty: Optional[DifficultyEnum] = DifficultyEnum.easy  # noqa: UP007
    tags: Optional[List[Tag]] = None  # noqa: UP006, UP007

    class Config:
        alias_generator = alias_generators.to_pascal
        populate_by_name = True  # needed if invoking to_pascal


class QuestionOut(QuestionIn):
    id: int

    class Config:
        alias_generator = alias_generators.to_pascal
        populate_by_name = True  # needed if invoking to_pascal
        json_schema_extra = {
            "example": {
                "Id": 1,
                "Question": "Sample question",
                "Solution": "Sample solution",
                "CorrectAnswer": "Answer",
                "Options": ["Option 1", "Option 2"],
                "Steps": [{"Title": "Step 1", "Result": "Result 1"}],
                "ImageUrl": "http://example.com/image.jpg",
                "Difficulty": "easy",
                "Tags": [{"Name": "math", "Slug": "math"}]
            }
        }


class QuestionPatchSchema(Schema):
    question: Optional[str] = None  # noqa: UP007
    solution: Optional[str] = None  # noqa: UP007
    correct_answer: Optional[str] = None  # noqa: UP007
    options: Optional[List[str]] = None  # noqa: UP006, UP007
    steps: Optional[List[SolutionStepSchema]] = None  # noqa: UP006, UP007
    image_url: Optional[str] = None  # noqa: UP007
    difficulty: Optional[DifficultyEnum] = None  # noqa: UP007
    tags: Optional[List[Tag]] = None  # noqa: UP006, UP007

    class Config:
        alias_generator = alias_generators.to_pascal
        populate_by_name = True
