from django.db.models.signals import post_save
from django.dispatch import receiver
from icecream import ic
from .models import UserOption, UserTrait, Score

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

    user_trait = UserTrait.objects.create(
        user=user,
        quiz=quiz,
        question=question,
        option=option,
        trait=traits or None
    )
    ic(user_trait.__dict__)
