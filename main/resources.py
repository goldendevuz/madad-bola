from import_export import resources
from .models import Quiz, Question, Option, Score, UserOption, UserQuiz


class QuizResource(resources.ModelResource):
    class Meta:
        model = Quiz


class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question


class OptionResource(resources.ModelResource):
    class Meta:
        model = Option


class ScoreResource(resources.ModelResource):
    class Meta:
        model = Score


class UserQuizResource(resources.ModelResource):
    class Meta:
        model = UserQuiz


class UserOptionResource(resources.ModelResource):
    class Meta:
        model = UserOption
        fields = ('user', 'question', 'option')
        export_order = ('user', 'question', 'option')

class UserTraitResource(resources.ModelResource):
    class Meta:
        model = UserOption
        fields = ('user', 'question', 'option')
        export_order = ('user', 'question', 'option')