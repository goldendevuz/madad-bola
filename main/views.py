import json
import requests
from django.http import JsonResponse
from icecream import ic
from rest_framework.decorators import api_view
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from telegraph import Telegraph

from .google import get_user_rows
from .utils import format_as_html, format_as_html_parents
from core.config import BASIC_AUTH_TOKEN

User = get_user_model()

SHEET_ID = '18r4BkP9NU7r2MLTG-oBPTSbVHkzZimVy96OhUXhskRM'

async def send_sms_message(html_message, phone):
    url = "https://positively-big-kingfish.ngrok-free.app/api/sms/"

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

async def send_sms_message_parents(html_message, phone):
    url = "https://positively-big-kingfish.ngrok-free.app/api/sms/"

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
    rows = get_user_rows(SHEET_ID)
    ic(rows)
    if not rows:
        return JsonResponse({'status': 'error', 'message': 'No data found'})
    row = rows[-1]
    ic(row)

    telegraph = Telegraph()
    telegraph.create_account(short_name='testbot')

    # Generate some test content
    title = request.data.get('title', 'Test Result')
    content = request.data.get('content', 'This is a test result.')

    # Telegraph API expects content in HTML
    response = telegraph.create_page(
        title=title,
        html_content=f'<p>{content}</p>',
    )
    html_message = format_as_html(row)
    html_message_parents = format_as_html_parents(row=row, path=response['path'])
    ic(html_message)

    # async_to_sync(send_sms_message)(html_message, phone=row[22])
    async_to_sync(send_sms_message_parents)(html_message_parents, phone=row[23])
    return JsonResponse({'status': 'sent', 'message': html_message})