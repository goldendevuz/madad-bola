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
from .models import UserOption, Option, UserTrait
from .utils import format_as_html, format_as_html_parents
from core.config import BASIC_AUTH_TOKEN

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
    'Authorization': f'Basic {BASIC_AUTH_TOKEN}',
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
    ic(rows)
    if not rows:
        return JsonResponse({'status': 'error', 'message': 'No data found'})

    traits = {}

    for trait in rows[2:]:
        traits[trait[0]] = trait[1]

    user, created = User.objects.get_or_create(phone=responses_row[23])

    for option_text in responses_row[1:21]:
        # Find the Option by text
        option = Option.objects.filter(text=option_text).first()
        if not option:
            print(f"Option with text '{option_text}' not found.")
            continue  # skip if option not found

        # Get the related question from option
        question = option.question

        # Create the UserOption linking user, question, and option
        user_option, created = UserOption.objects.get_or_create(
            user=user,
            question=question,
            option=option
        )

    user_traits_qs = UserTrait.objects.filter(user=user)
    all_traits_lists = user_traits_qs.values_list('trait', flat=True)
    unique_traits = set(chain.from_iterable(filter(None, all_traits_lists)))
    unique_traits_list = list(unique_traits)
    ic(user_traits_qs)
    ic(all_traits_lists)
    ic(unique_traits)
    ic(unique_traits_list)

    full_name = responses_row[21]

    parents_message = f"Farzandingiz {full_name}  pulga nisbatan quyidagicha nuqtai nazari aniqlandi: "
    user_traits = ",".join(unique_traits_list)
    parents_message += user_traits

    user_feedbacks = []

    for trait in unique_traits_list:
        user_feedbacks.append(traits.get(trait))

    child_message = f"Sizda:\n"
    child_message = ",".join(user_feedbacks)

    telegraph = Telegraph()
    telegraph.create_account(short_name='testbot')

    # Generate some test content
    title = request.data.get('title', 'Test Result')
    # content = request.data.get('content', 'This is a test result.')

    content = parents_message

    # Telegraph API expects content in HTML
    response = telegraph.create_page(
        title=title,
        html_content=f'<p>{content}</p>',
    )
    html_message_parents = format_as_html_parents(row=responses_row, path=response['path'])
    ic(html_message_parents)

    content = child_message
    response = telegraph.create_page(
        title=title,
        html_content=f'<p>{content}</p>',
    )
    html_message = format_as_html(responses_row, path=response['path'])
    ic(html_message)

    async_to_sync(send_sms_message)(html_message, phone=responses_row[22])
    async_to_sync(send_sms_message)(html_message_parents, phone=responses_row[23])
    return JsonResponse({'status': 'sent', 'message': html_message})