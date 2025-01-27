# Backend4Sat

My implementation for a tasked backend developer position

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Overview

This project provides a Django-based API for managing multiple-choice questions. It uses Ninja for routing, Django models for data structures, and includes endpoints for creating, reading, updating, and deleting questions, options, steps, and tags.

## Key Files

- `api.py`: Defines API endpoints (GET, POST, PATCH, DELETE) using Ninja.
- `models.py`: Defines the *Question*, *Option*, *SolutionStep*, and *Tag* models.
- `schemas.py` : Contains Pydantic schemas for request/
response validation.

## How to Run

### **Prerequisite**

- Docker, if you don't have it yet, follow the [installation instructions](https://docs.docker.com/get-started/get-docker/#supported-platforms);

### Running Locally with Docker

1. Open your terminal and clone this repo

    ```sh
    % git clone https://github.com/jericho1050/backend4sat.git
    ```

2. Change to cloned directory then build image

   ```bash
   % cd backend4sat 
   % docker compose -f docker-compose.local.yml build
   ```

3. It might take a while, once finished building

   ```bash
   % docker compose -f docker-compose.local.yml up
   ```

4. *(Optional)* ingest sample mock data in `backend_sat_task/data/questions.json`, create questions from JSON file

    ```bash
    % docker compose -f docker-compose.local.yml run --rm django python manage.py ingest_questions
    ```

5. That's it! you can now visit `http://localhost:8000` or `http://localhost:8000/api/v0/docs` for the interactive openapi docs

**Note**: In order to get the `/upload-image` route working locally, you need to define values here in `.django` env variables using the AWS S3 service

```sh
DJANGO_AWS_ACCESS_KEY_ID=YOUR_ACESS_KEY_ID
DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
DJANGO_AWS_STORAGE_BUCKET_NAME=YOUR_STORAGE_BUCKET_NAME
DJANGO_AWS_S3_REGION_NAME=YOUR_S3_REGION_NAME
# I am using cloudfront service, so it's URL will be here
DJANGO_AWS_S3_CUSTOM_DOMAIN=YOUR_CUSTOM_DOMAIN
```

## Endpoints

1. GET `/api/v0/questions`  

   Returns paginated list of all questions.

2. GET `/api/v0/question/{question_id}`  

   Returns details of a question by ID.

3. POST `/api/v0/questions`  

   Creates a new question (requires API key).

4. PATCH `/api/v0/question/{question_id}`  

   Partially updates a question (requires API key).

5. DELETE `/api/v0/question/{question_id}`  

   Deletes a question (requires API key).

## Sample Calls

```bash
# 1. Retrieve all questions (paginated):
curl -X GET "https://backend4sat.site/api/v0/questions"

# 2. Retrieve a single question by ID:
curl -X GET "https://backend4sat.site/api/v0/question/1"

# 3. Create a new question:
curl -X POST -H "Content-Type: application/json" \
-d '{
  "Question": "What is 1+1?",
  "Solution": "Add numbers",
  "CorrectAnswer": "2",
  "Options": ["1", "2"],
  "Steps": [{"Title": "Step 1", "Result": "Add 1 and 1", "StepNumber": 1}]
}' \
"https://backend4sat.site/api/v0/questions?api_key=YOUR_API_KEY"

# 4. Partially update an existing question:
curl -X PATCH -H "Content-Type: application/json" \
-d '{
  "Question": "Updated question text"
}' \
"https://backend4sat.site/api/v0/question/1?api_key=YOUR_API_KEY"

# 5. Delete a question:
curl -X DELETE "https://backend4sat.site/api/v0/question/1?api_key=YOUR_API_KEY"
```

Use valid UUID-based API keys when making requests to protected endpoints.

## Basic Commands

### Setting Up Your Users

- To create a **superuser account**, use this command per the [django-cookiecutter documentation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally-docker.html#execute-management-commands):

    ```sh
    % docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser
    ```

### Type checks

Running type checks with mypy in devcontainer:

```sh
/app$ mypy backend_sat_task
```

#### Running tests

```sh
# in the devcontainer
$ python manage.py test
```

```sh
# in your terminal
% docker compose -f docker-compose.local.yml run --rm django python manage.py test
```

## Deployment

TODO

### Docker

See detailed [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html).
