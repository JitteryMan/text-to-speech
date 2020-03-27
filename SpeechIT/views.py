from django.shortcuts import render
from django.http import HttpResponse
from gtts import gTTS


def index(request):
    return render(request, 'SpeechIT/homepage.html', {'path': request.path})


def to_speech(request, text_data):
    text_data = request.POST['qtext']
    return render(request, 'SpeechIT/download.html', {'text': text_data, 'ip': request.META.get('HTTP_X_FORWARDED_FOR'),
                                                      'ip2': request.META.get('REMOTE_ADDR')})
