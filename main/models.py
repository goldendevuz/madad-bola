from django.db import models
from django.contrib.auth import get_user_model

from shared.models import BaseModel

User = get_user_model()

class Quiz(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Question(BaseModel):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, unique=True)
    order = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 21)], default=1)

    def __str__(self):
        return f"{self.order} {self.text}"
    
    class Meta:
        ordering = ['order']
        unique_together = ('quiz', 'text')
    

class Option(BaseModel):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, unique=True)
    order = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 4)], default=1)

    def __str__(self):
        return f"{self.question.order}.{self.order} {self.text}"
    
    class Meta:
        ordering = ['question', 'order']
        unique_together = ('question', 'text')


class Score(BaseModel):
    quiz = models.ForeignKey(Quiz, related_name='scores', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name='scores', on_delete=models.CASCADE)
    trait = models.CharField(
        max_length=50,
        choices=[
            ('tejamkorlik', 'Tejamkorlik'),
            ('isrofgarchilik', 'Isrofgarchilik'),
            ('passivlik', 'Passivlik'),
            ('motivatsiya', 'Motivatsiya'),
            ('salbiy_dunyoqarash', 'Salbiy dunyoqarash'),
            ('ijobiy_dunyoqarash', 'Ijobiy dunyoqarash'),
            ('tashqi_taasirga_bogliqlik', "Tashqi ta'sirga bog'liqlik"),
            ('ota_ona_tarbiyasi', "Ota-ona tarbiyasi"),
            ('ota_ona_muammolari', "Ota-ona muammolari"),
            ('ijtimoiy_bosim', 'Ijtimoiy bosim'),
            ('savodxonlik', 'Savodxonlik'),
            ('erkinlik', 'Erkinlik'),
            ('masuliyat', "Mas'uliyat"),
            ('nazorat_yoqligi', "Nazorat yo'qligi"),
            ('pul_idealizatsiyasi', 'Pul idealizatsiyasi'),
            ('barqarorlik', 'Barqarorlik'),
        ],
        default='tejamkorlik',
    )

    def __str__(self):
        return self.quiz.title

    class Meta:
        unique_together = ('quiz', 'option', 'trait')
        ordering = ['quiz', 'option', 'trait']


class UserQuiz(BaseModel):
    user = models.ForeignKey(User, related_name='quizzes', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='user_quizzes', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"User {self.user_id} completed {self.quiz.title}: {self.completed}"


class UserOption(BaseModel):
    user = models.ForeignKey(User, related_name='user_options', on_delete=models.CASCADE)
    # quiz = models.ForeignKey(Quiz, related_name='user_options', on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(UserQuiz, related_name='user_options', on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Question, related_name='user_options', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name='user_options', on_delete=models.CASCADE)

    def __str__(self):
        return f"User {self.user_id} selected {self.option.text}"

    class Meta:
        # unique_together = ('user', 'question', 'option')
        ordering = ['user', 'question', 'option']


class UserTrait(BaseModel):
    user = models.ForeignKey(User, related_name='user_traits', on_delete=models.CASCADE)
    quiz = models.ForeignKey(UserQuiz, related_name='user_traits', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='user_traits', on_delete=models.CASCADE)
    option = models.ForeignKey(UserOption, related_name='user_traits', on_delete=models.CASCADE)
    trait = models.JSONField(null=True)

    def __str__(self):
        return f"User {self.user_id} trait {self.trait}"