from django.urls import path
from .views import index, to_speech

app_name = 'SpeechIT'
urlpatterns = [
    path('', index, name='index'),
    path('<str:text_data>', to_speech, name='to_speech'),
]
