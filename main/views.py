import json
import requests
from itertools import chain
from django.http import JsonResponse
from icecream import ic
from rest_framework.decorators import api_view
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from telegraph import Telegraph

from .google import get_user_rows, get_result_rows
from .models import UserOption, Option, UserTrait, UserQuiz, Quiz
from .utils import format_as_html, format_as_html_parents
from core.config import BEARER_AUTH_TOKEN

User = get_user_model()

SHEET_ID = '18r4BkP9NU7r2MLTG-oBPTSbVHkzZimVy96OhUXhskRM'

async def send_sms_message(html_message, phone):
    url = "https://piglet-factual-mentally.ngrok-free.app/api/sms/"

    payload = json.dumps({
    "number": phone.replace("+998", ""),
    "text": f"""{html_message}""",
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {BEARER_AUTH_TOKEN}',
    }
    ic(payload)
    ic(headers)

    response = requests.request("POST", url, headers=headers, data=payload)
    ic(response)
    ic(response.json())
    return response.json()

@api_view(['POST'])
def send_latest_google_response(request):
    responses_rows = get_user_rows(SHEET_ID)
    ic(responses_rows)
    if not responses_rows:
        return JsonResponse({'status': 'error', 'message': 'No data found'})
    responses_row = responses_rows[-1]
    ic(responses_row)

    rows = get_result_rows(SHEET_ID)
    # ic(rows)
    if not rows:
        return JsonResponse({'status': 'error', 'message': 'No data found'})

    traits = {}

    for trait in rows[2:]:
        traits[trait[0]] = trait[1]
    # ic(traits)
    if responses_row[22]:
        user, created = User.objects.get_or_create(full_name=responses_row[21], student_phone=responses_row[22],
                                               parents_phone=responses_row[23])
    else:
        user, created = User.objects.get_or_create(full_name=responses_row[21], parents_phone=responses_row[23])

    # ic(user.__dict__)
    quiz = Quiz.objects.get(title="Biznesbola")
    # ic(quiz.__dict__)
    user_quiz = UserQuiz.objects.create(user=user, quiz=quiz)
    # ic(user_quiz.__dict__)

    user_options_count = 0
    for option_text in responses_row[1:21]:
        if option_text:
            # ic(option_text)
            # for opt in Option.objects.all():
            #     ic(opt)
                # ic(opt)
            # Find the Option by text
            option = Option.objects.get(text=option_text)

            # Get the related question from option
            question = option.question

            # Create the UserOption linking user, question, and option
            UserOption.objects.get_or_create(
                user=user,
                quiz=user_quiz,
                question=question,
                option=option
            )
            # ic(user_option.__dict__)
            user_options_count += 1

    user_traits_qs = UserTrait.objects.filter(user=user, quiz=user_quiz)
    # ic(user_traits_qs)

    unique_traits = set()
    for ut in user_traits_qs:
        for trait in ut.trait.split(", "):
            unique_traits.add(trait)
        ic(unique_traits)

    full_name = responses_row[21]
    # ic(full_name)

    parents_message = f"Farzandingiz {full_name}  pulga nisbatan quyidagicha nuqtai nazari aniqlandi: "
    user_traits = ", ".join(unique_traits)
    # ic(user_traits)
    parents_message += f'<p>{user_traits}</p>'
    # ic(parents_message)

    user_feedbacks = []

    for trait in unique_traits:
        # ic(trait)
        user_feedbacks.append(traits.get(trait))
    # ic(user_feedbacks)

    child_message = f"Sizda: "
    for feedback in user_feedbacks:
        child_message += f'<p>{feedback}</p>'
    # ic(child_message)

    telegraph = Telegraph()
    telegraph.create_account(short_name='testbot')

    # Generate some test content
    title = request.data.get('title', 'Farzandingizning test natijangiz')
    # content = request.data.get('content', 'This is a test result.')

    content = parents_message
    # ic(content)

    # Telegraph API expects content in HTML
    response = telegraph.create_page(
        title=title,
        html_content=f'<p>{content}</p>',
    )
    # ic(response)
    html_message_parents = format_as_html_parents(row=responses_row, path=response['path'])
    ic(html_message_parents)

    title = request.data.get('title', 'Sizning test natijangiz')
    content = child_message
    response = telegraph.create_page(
        title=title,
        html_content=f'<p>{content}</p>',
    )
    # ic(response)
    html_message = format_as_html(responses_row, path=response['path'])
    ic(html_message)

    async_to_sync(send_sms_message)(html_message_parents, phone=responses_row[23])
    if responses_row[22]:
        async_to_sync(send_sms_message)(html_message, phone=responses_row[22])
    else:
        async_to_sync(send_sms_message)(html_message, phone=responses_row[23])

    if user_options_count == 20:
        user_quiz.completed = True
    return JsonResponse({'status': 'sent', 'message': html_message})