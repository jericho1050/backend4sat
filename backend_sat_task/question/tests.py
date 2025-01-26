import logging
import os
from io import BytesIO

os.environ["NINJA_SKIP_REGISTRY"] = "yes"
import uuid

from django.test import Client
from django.test import TestCase
from ninja.testing import TestClient

from backend_sat_task.question.api import api
from backend_sat_task.question.models import Option
from backend_sat_task.question.models import Question
from backend_sat_task.question.models import SolutionStep
from backend_sat_task.question.models import Tag
from backend_sat_task.question.models import User
from django.core.exceptions import ValidationError


class TestQuestionAPI(TestCase):
    def setUp(self):
        self.api_key = uuid.uuid4()
        self.client = TestClient(api)
        # Create user with required fields
        self.user = User.objects.create(
            username="testuser",  # Required
            email="test@example.com",  # Required
            password="testpass123",  # Required
            api_key=self.api_key,
        )
        self.valid_payload = {
            "Question": "What is 2+2?",
            "Solution": "Add the numbers",
            "CorrectAnswer": "4",
            "Difficulty": "easy",
            "Options": ["2", "3", "4", "5"],
            "Steps": [
                {
                    "Title": "Step 1",
                    "Result": "Add 2 and 2",
                    "ImageUrl": None,
                    "StepNumber": 1,
                }
            ],
            "Tags": [{"Name": "Math", "Slug": "math"}],
            "ImageUrl": None,
        }
        # Create 15 questions
        for i in range(15):
            Question.objects.create(
                question=f"Test Question {i}",
                solution=f"Solution {i}",
                correct_answer=str(i),
                difficulty="easy",
            )

    def test_create_question_success(self):
        response = self.client.post(
            f"/questions?api_key={self.api_key}",  # Updated path
            json=self.valid_payload,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn("Id", data)
        self.assertEqual(data["Question"], self.valid_payload["Question"])
        self.assertEqual(data["Solution"], self.valid_payload["Solution"])
        self.assertEqual(data["CorrectAnswer"], self.valid_payload["CorrectAnswer"])
        self.assertEqual(len(data["Options"]), 4)
        self.assertEqual(len(data["Steps"]), 1)
        self.assertEqual(len(data["Tags"]), 1)

        question = Question.objects.get(id=data["Id"])
        self.assertEqual(question.question, self.valid_payload["Question"])
        self.assertEqual(question.options.count(), 4)
        self.assertEqual(question.steps.count(), 1)
        self.assertEqual(question.tags.count(), 1)

    def test_create_question_unauthorized(self):
        response = self.client.post(
            "/questions",  # Updated path
            json=self.valid_payload,
            headers={},
        )
        self.assertEqual(response.status_code, 401)

    def test_create_question_missing_required_fields(self):
        invalid_payload = {
            "Question": "What is 2+2?",
        }
        response = self.client.post(
            f"/questions?api_key={self.api_key}",  # Updated path
            json=invalid_payload,
        )
        self.assertEqual(response.status_code, 422)

    def test_create_question_without_required_fields(self):
        minimal_payload = {
            "Question": "What is 2+2?",
            "Solution": "Add the numbers",
            "CorrectAnswer": "4",
            "Difficulty": "Easy",
            "Options": ["2", "3", "4", "5"],
        }
        response = self.client.post(
            f"/questions?api_key={self.api_key}",  # Updated path
            json=minimal_payload,
        )
        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(
            response.data,
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "payload", "Steps"],
                        "msg": "Field required",
                    },
                    {
                        "type": "enum",
                        "loc": ["body", "payload", "Difficulty"],
                        "msg": "Input should be 'easy', 'medium' or 'hard'",
                        "ctx": {"expected": "'easy', 'medium' or 'hard'"},
                    },
                ]
            },
        )

    # def test_upload_image(self):
    #     # Create test image data
    #     image_io = BytesIO(b"some initial binary data: \x00\x01")
    #     image_io.seek(0)

    #     # Create binary content
    #     binary_content = image_io.getvalue()

    #     response = self.client.post(
    #         f"/upload-image?api_key={self.api_key}",
    #         files={"file": str(binary_content)},
    #     )

    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("url", response.json())

    def test_get_questions_success(self):
        response = self.client.get("/questions", query={"api_key": str(self.api_key)})

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Check response structure
        self.assertIn("items", data)
        self.assertEqual(len(data["items"]), 15)

        # Check first question matches setup data
        first_question = data["items"][0]
        self.assertIn("Id", first_question)
        self.assertEqual(first_question["Question"], "Test Question 0")
        self.assertEqual(first_question["Solution"], "Solution 0")
        self.assertEqual(first_question["CorrectAnswer"], "0")
        self.assertEqual(first_question["Difficulty"], "easy")

        # These should be empty as not created in setup
        self.assertEqual(first_question["Options"], [])
        self.assertEqual(first_question["Steps"], [])
        self.assertEqual(first_question["Tags"], [])

    def test_get_questions_pagination(self):
        response = self.client.get(
            "/questions", query={"api_key": str(self.api_key), "page": 1, "size": 10}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn("items", data)
        self.assertEqual(len(data["items"]), 15)
        self.assertIn("count", data)
        self.assertEqual(data["count"], 15)

    def test_get_questions_empty(self):
        Question.objects.all().delete()
        response = self.client.get("/questions", query={"api_key": str(self.api_key)})

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn("items", data)
        self.assertEqual(len(data["items"]), 0)
        self.assertIn("count", data)
        self.assertEqual(data["count"], 0)

    def test_get_question_success(self):
        # Create question with related data
        question = Question.objects.create(
            question="Test Question",
            solution="Test Solution",
            correct_answer="42",
            difficulty="easy",
        )

        # Add options
        for i in range(4):
            Option.objects.create(question=question, option_text=f"Option {i}")

        # Add step
        SolutionStep.objects.create(
            question=question, title="Step 1", result="Result 1", step_number=1
        )

        # Add tag
        tag = Tag.objects.create(name="Math", slug="math")
        question.tags.add(tag)

        response = self.client.get(f"/question/{question.id}")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Check response structure
        self.assertEqual(data["Id"], question.id)
        self.assertEqual(data["Question"], "Test Question")
        self.assertEqual(data["Solution"], "Test Solution")
        self.assertEqual(data["CorrectAnswer"], "42")
        self.assertEqual(data["Difficulty"], "easy")

        # Check related data
        self.assertEqual(len(data["Options"]), 4)
        self.assertEqual(len(data["Steps"]), 1)
        self.assertEqual(len(data["Tags"]), 1)

        # Verify first option
        self.assertEqual(data["Options"][0], "Option 0")

        # Verify step
        step = data["Steps"][0]
        self.assertEqual(step["Title"], "Step 1")
        self.assertEqual(step["Result"], "Result 1")

        # Verify tag
        tag = data["Tags"][0]
        self.assertEqual(tag["Name"], "Math")
        self.assertEqual(tag["Slug"], "math")

    def test_get_question_not_found(self):
        response = self.client.get("/question/99999")
        self.assertEqual(response.status_code, 404)

    def test_get_question_without_api_key_param(self):
        question = Question.objects.first()
        response = self.client.get(f"/question/{question.id}")
        self.assertEqual(response.status_code, 200)

    def test_patch_question_success(self):
        # Create initial question
        question = Question.objects.create(
            question="Original Question",
            solution="Original Solution",
            correct_answer="42",
            difficulty="easy",
        )

        # Create initial tag
        tag = Tag.objects.create(name="Updated", slug="updated")

        patch_payload = {
            "Question": "Updated Question",
            "Solution": "Updated Solution",
            "CorrectAnswer": "24",
            "Difficulty": "medium",
            "Options": ["1", "2", "24", "4"],
            "Steps": [
                {
                    "Title": "New Step 1",
                    "Result": "New Result 1",
                    "ImageUrl": None,
                    "StepNumber": 1,
                }
            ],
            "Tags": [{"Name": tag.name, "Slug": tag.slug}],
        }

        response = self.client.patch(
            f"/question/{question.id}?api_key={self.api_key}",
            json=patch_payload,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Verify updated fields
        self.assertEqual(data["Question"], patch_payload["Question"])
        self.assertEqual(data["Solution"], patch_payload["Solution"])
        self.assertEqual(data["CorrectAnswer"], patch_payload["CorrectAnswer"])
        self.assertEqual(data["Difficulty"], patch_payload["Difficulty"])

        # Verify relations
        self.assertEqual(len(data["Options"]), 4)
        self.assertEqual(len(data["Steps"]), 1)
        self.assertEqual(len(data["Tags"]), 1)
        self.assertEqual(data["Tags"][0]["Name"], tag.name)
        self.assertEqual(data["Tags"][0]["Slug"], tag.slug)

    def test_patch_question_partial(self):
        question = Question.objects.create(
            question="Original Question",
            solution="Original Solution",
            correct_answer="42",
            difficulty="easy",
        )

        patch_payload = {"Question": "Updated Question", "Difficulty": "hard"}

        response = self.client.patch(
            f"/question/{question.id}?api_key={self.api_key}",
            json=patch_payload,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Check updated fields
        self.assertEqual(data["Question"], "Updated Question")
        self.assertEqual(data["Difficulty"], "hard")
        # Check unchanged fields
        self.assertEqual(data["Solution"], "Original Solution")
        self.assertEqual(data["CorrectAnswer"], "42")

    def test_patch_question_unauthorized(self):
        question = Question.objects.create(
            question="Test Question",
            solution="Test Solution",
            correct_answer="42",
            difficulty="easy",
        )

        response = self.client.patch(
            f"/question/{question.id}?api_key=59f9eec7-3ce6-4bc9-80d6-b6788b88a36c",
            json={"Question": "Unauthorized Update"},
        )

        self.assertEqual(response.status_code, 401)

    def test_patch_question_not_found(self):
        response = self.client.patch(
            f"/question/99999?api_key={self.api_key}",
            json={"Question": "Not Found"},
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_question_success(self):
        # Create question to delete
        question = Question.objects.create(
            question="Delete me",
            solution="Solution",
            correct_answer="42",
            difficulty="easy",
        )
        question_id = question.id

        response = self.client.delete(f"/question/{question.id}?api_key={self.api_key}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"sucess": True})

        # Verify question is deleted from database
        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(id=question_id)

    def test_delete_question_unauthorized(self):
        question = Question.objects.first()
        response = self.client.delete(f"/question/{question.id}")
        self.assertEqual(response.status_code, 401)

        # Verify question still exists
        self.assertTrue(Question.objects.filter(id=question.id).exists())

    def test_delete_question_not_found(self):
        response = self.client.delete(
            f"/question/9999999999?api_key={self.api_key}",
        )
        self.assertEqual(response.status_code, 404)
