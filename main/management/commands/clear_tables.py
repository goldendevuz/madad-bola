from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Deletes all rows from specified tables'

    def handle(self, *args, **options):
        model_names = [
            'main.UserQuiz',
            'main.UserOption',
            'main.UserTrait',
            # Add more as needed
        ]

        for model_path in model_names:
            app_label, model_name = model_path.split('.')
            model = apps.get_model(app_label, model_name)

            if model:
                model.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'Cleared: {model_path}'))
            else:
                self.stdout.write(self.style.WARNING(f'Model not found: {model_path}'))
