from django.urls import path

from .views import send_latest_google_response

urlpatterns = [
    path('google-sheet-webhook/', send_latest_google_response, name='google-sheet-webhook'),
]