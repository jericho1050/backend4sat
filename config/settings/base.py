# ruff: noqa: ERA001, E501
"""Base settings to build other settings files upon."""

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# backend_sat_task/
APPS_DIR = BASE_DIR / "backend_sat_task"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#languages
# from django.utils.translation import gettext_lazy as _
# LANGUAGES = [
#     ('en', _('English')),
#     ('fr-fr', _('French')),
#     ('pt-br', _('Portuguese')),
# ]
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",
    "tailwind",
    "theme",
    "corsheaders",
]

LOCAL_APPS = [
    # Your stuff: custom apps go here
    "backend_sat_task.question",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "backend_sat_task.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "question.User"

# # https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
# LOGIN_REDIRECT_URL = "users:redirect"
# # https://docs.djangoproject.com/en/dev/ref/settings/#login-url
# LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [str(APPS_DIR / "templates")],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Jericho Wenzel Serrano""", "jerichoserrano@backend4sat.site")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
# https://cookiecutter-django.readthedocs.io/en/latest/settings.html#other-environment-settings


# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

REDIS_URL = env("REDIS_URL", default="redis://redis:6379/0")
REDIS_SSL = REDIS_URL.startswith("rediss://")


# Your stuff...
# ------------------------------------------------------------------------------
TAILWIND_APP_NAME = "theme"
NPM_BIN_PATH = "/usr/bin/npm"


# Allow all origins
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
# Allow all HTTP methods
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# customColorPalette = [  # noqa: N816
#     {"color": "hsl(4, 90%, 58%)", "label": "Red"},
#     {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
#     {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
#     {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
#     {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
#     {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
# ]

# # CKEDITOR_5_CUSTOM_CSS = "path_to.css"  # optional
# # CKEDITOR_5_FILE_STORAGE = "path_to_storage.CustomStorage"  # optional
# CKEDITOR_5_CONFIGS = {
#     "default": {
#         "toolbar": [
#             "heading",
#             "|",
#             "bold",
#             "italic",
#             "link",
#             "bulletedList",
#             "numberedList",
#             "blockQuote",
#             "imageUpload",
#         ],
#     },
#     "extends": {
#         "blockToolbar": [
#             "paragraph",
#             "heading1",
#             "heading2",
#             "heading3",
#             "|",
#             "bulletedList",
#             "numberedList",
#             "|",
#             "blockQuote",
#         ],
#         "toolbar": [
#             "heading",
#             "|",
#             "outdent",
#             "indent",
#             "|",
#             "bold",
#             "italic",
#             "link",
#             "underline",
#             "strikethrough",
#             "code",
#             "subscript",
#             "superscript",
#             "highlight",
#             "|",
#             "codeBlock",
#             "sourceEditing",
#             "insertImage",
#             "bulletedList",
#             "numberedList",
#             "todoList",
#             "|",
#             "blockQuote",
#             "imageUpload",
#             "|",
#             "fontSize",
#             "fontFamily",
#             "fontColor",
#             "fontBackgroundColor",
#             "mediaEmbed",
#             "removeFormat",
#             "insertTable",
#         ],
#         "image": {
#             "toolbar": [
#                 "imageTextAlternative",
#                 "|",
#                 "imageStyle:alignLeft",
#                 "imageStyle:alignRight",
#                 "imageStyle:alignCenter",
#                 "imageStyle:side",
#                 "|",
#             ],
#             "styles": [
#                 "full",
#                 "side",
#                 "alignLeft",
#                 "alignRight",
#                 "alignCenter",
#             ],
#         },
#         "table": {
#             "contentToolbar": [
#                 "tableColumn",
#                 "tableRow",
#                 "mergeTableCells",
#                 "tableProperties",
#                 "tableCellProperties",
#             ],
#             "tableProperties": {
#                 "borderColors": customColorPalette,
#                 "backgroundColors": customColorPalette,
#             },
#             "tableCellProperties": {
#                 "borderColors": customColorPalette,
#                 "backgroundColors": customColorPalette,
#             },
#         },
#         "heading": {
#             "options": [
#                 {
#                     "model": "paragraph",
#                     "title": "Paragraph",
#                     "class": "ck-heading_paragraph",
#                 },
#                 {
#                     "model": "heading1",
#                     "view": "h1",
#                     "title": "Heading 1",
#                     "class": "ck-heading_heading1",
#                 },
#                 {
#                     "model": "heading2",
#                     "view": "h2",
#                     "title": "Heading 2",
#                     "class": "ck-heading_heading2",
#                 },
#                 {
#                     "model": "heading3",
#                     "view": "h3",
#                     "title": "Heading 3",
#                     "class": "ck-heading_heading3",
#                 },
#             ],
#         },
#     },
#     "list": {
#         "properties": {
#             "styles": "true",
#             "startIndex": "true",
#             "reversed": "true",
#         },
#     },
# }

# # Define a constant in settings.py to specify file upload permissions
# CKEDITOR_5_FILE_UPLOAD_PERMISSION = (
#     "any"  # Possible values: "staff", "authenticated", "any"
# )

# CK_EDITOR_5_UPLOAD_FILE_VIEW_NAME = "custom_upload_file"
