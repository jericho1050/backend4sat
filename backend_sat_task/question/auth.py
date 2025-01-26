import logging

from django.http import JsonResponse
from ninja.security import APIKeyQuery

from backend_sat_task.question.models import User


class ApiKey(APIKeyQuery):
    param_name = "api_key"

    def authenticate(self, request, key):
        logging.error("Authentication attempt")

        if not key:
            logging.error("No API key provided")
            return None

        try:
            user = User.objects.get(api_key=key)
            logging.info(f"Authenticated user: {user.username}")
            return user
        except User.DoesNotExist:
            logging.error("Invalid API key")
            return None

    # Remove _handle_error method as it breaks the auth flow
