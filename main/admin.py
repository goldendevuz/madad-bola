from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Quiz, Question, Option, Score, UserOption, UserQuiz, UserTrait
from .resources import (
    QuizResource, QuestionResource, OptionResource,
    ScoreResource, UserOptionResource, UserQuizResource, UserTraitResource
)


@admin.register(Quiz)
class QuizAdmin(ImportExportModelAdmin):
    resource_class = QuizResource
    list_display = [field.name for field in Quiz._meta.fields]


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    list_display = [field.name for field in Question._meta.fields]
    list_display_links = list_display


@admin.register(Option)
class OptionAdmin(ImportExportModelAdmin):
    resource_class = OptionResource
    list_display = ['text'] #[field.name for field in Option._meta.fields]
    list_display_links = list_display


@admin.register(Score)
class ScoreAdmin(ImportExportModelAdmin):
    resource_class = ScoreResource
    list_display = [field.name for field in Score._meta.fields]
    list_filter = ['option__text']


@admin.register(UserQuiz)
class UserQuizAdmin(ImportExportModelAdmin):
    resource_class = UserQuizResource
    list_display = [field.name for field in UserQuiz._meta.fields]
    readonly_fields = ["completed"]


@admin.register(UserOption)
class UserOptionAdmin(ImportExportModelAdmin):
    resource_class = UserOptionResource
    list_display = [field.name for field in UserOption._meta.fields]


@admin.register(UserTrait)
class UserTraitAdmin(ImportExportModelAdmin):
    resource_class = UserTraitResource
    list_display = [field.name for field in UserTrait._meta.fields]