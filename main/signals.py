from django.db.models.signals import post_save
from django.dispatch import receiver
from icecream import ic
from .models import UserOption, UserTrait, Score, UserQuiz


@receiver(post_save, sender=UserOption)
def create_user_trait_from_option(sender, instance, created, **kwargs):
    # if not created:
    #     return

    user = instance.user
    question = instance.question
    option = instance.option
    quiz = getattr(question, 'quiz', None)

    if not quiz:
        return

    # Fetch all matching score objects
    score_qs = Score.objects.filter(quiz=quiz, option=option)
    ic(score_qs)

    traits = ", ".join([score.get_trait_display() for score in score_qs])

    user_quiz = UserQuiz.objects.filter(
        user=user, quiz=quiz, completed=False
    ).order_by('-created').first()

    if not user_quiz:
        user_quiz = UserQuiz.objects.create(
            user=user, quiz=quiz, completed=False
        )

    user_trait = UserTrait.objects.filter(
        user=user,
        quiz=user_quiz,
        question=question,
        option=instance,
        trait=traits or None
    ).order_by('-created').first()

    if not user_trait:
        user_trait = UserTrait.objects.create(
            user=user,
            quiz=user_quiz,
            question=question,
            option=instance,
            trait=traits or None
        )

    ic(user_trait.__dict__)
