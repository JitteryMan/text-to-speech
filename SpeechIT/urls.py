from django.urls import path
from .views import index, to_speech, audio_page

app_name = 'SpeechIT'
urlpatterns = [
    path('', index, name='index'),
    path('spoken/', to_speech, name='to_speech'),
    path('spoken/<str:hash_>', audio_page, name='audio_page'),
]
