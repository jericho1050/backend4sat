from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Option
from .models import Question
from .models import SolutionStep
from .models import Tag
from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("API Key", {"fields": ("api_key",)}),)  # noqa: RUF005
    readonly_fields = ("api_key",)
    list_display = ("username", "email", "api_key", "is_staff", "is_active")


# Fix registration syntax
admin.site.register(User, CustomUserAdmin)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Tag)
admin.site.register(SolutionStep)
