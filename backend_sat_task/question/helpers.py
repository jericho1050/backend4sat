import os
from uuid import uuid4

from django.conf import settings
from ninja.files import UploadedFile


def save_uploaded_file(uploaded_file: UploadedFile) -> str:
    """Save file and return URL path"""
    ext = os.path.splitext(uploaded_file.name)[1]  # noqa: PTH122
    filename = f"{uuid4()}{ext}"
    file_path = os.path.join("questions", filename)  # noqa: PTH118
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)  # noqa: PTH118

    # Ensure directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)  # noqa: PTH103, PTH120

    with open(full_path, "wb+") as destination:  # noqa: PTH123
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return f"{settings.MEDIA_URL}{file_path}"
