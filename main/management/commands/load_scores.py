import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from icecream import ic

from main.models import Quiz, Option, Score

# Path to core/data/service-account.json
SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, 'core', 'data', 'service-account.json')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

traits = {
    1: 'tejamkorlik',
    2: 'isrofgarchilik',
    3: 'passivlik',
    4: 'motivatsiya',
    5: 'salbiy_dunyoqarash',
    6: 'ijobiy_dunyoqarash',
    7: 'tashqi_taasirga_bogliqlik',
    8: 'ota_ona_tarbiyasi',
    9: 'ota_ona_muammolari',
    10: 'ijtimoiy_bosim',
    11: 'savodxonlik',
    12: 'erkinlik',
    13: 'masuliyat',
    14: 'nazorat_yoqligi',
    15: 'pul_idealizatsiyasi',
    16: 'barqarorlik',
}

def get_google_services():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    sheets_service = build('sheets', 'v4', credentials=creds)
    return creds, sheets_service

def get_user_rows(sheet_id, sheet_name="scoring"):
    range_name = f"{sheet_name}!A2:R62"
    _, sheets_service = get_google_services()

    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=range_name
    ).execute()

    return result.get("values", [])

class Command(BaseCommand):
    help = "Loads latest user traits from Google Sheets"

    def add_arguments(self, parser):
        parser.add_argument('sheet_id', type=str, help='Google Sheet ID')

    def handle(self, *args, **options):
        sheet_id = options['sheet_id']
        rows = get_user_rows(sheet_id)

        if not rows:
            self.stdout.write(self.style.ERROR('No data found'))
            return

        for row in rows:
            # ic(row)
            # Assumes the option order is 1:1 with trait index (first 2 cols = timestamp, name)
            for index, score in enumerate(row[2:], start=1):
                if score == '1':
                    trait_key = traits.get(index)
                    if not trait_key:
                        self.stdout.write(self.style.WARNING(f"Trait not found for index {index}"))
                        continue

                    try:
                        # ic(row[1])
                        # You must ensure Option order matches spreadsheet order!
                        option = Option.objects.get(text=row[1])  # or `.filter(trait=trait_key).first()` depending on schema
                        quiz = option.question.quiz
                        obj = Score.objects.create(
                            quiz=quiz,
                            option=option,
                            trait=trait_key,
                            score=True
                        )
                        # ic(quiz.id, option.id, trait_key, obj.__dict__)
                    except IntegrityError:
                        pass
                    except Option.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Option not found for index {index}"))
                        self.stdout.write(self.style.WARNING(row))
