from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponseRedirect
from gtts import gTTS
from .models import Post
import hashlib
import os


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')


def create_mp3(text, lang: str):
    mp3 = None
    if text:
        mp3 = gTTS(text=text, lang=lang)
    return mp3


def get_hash(text: str) -> str:
    return hashlib.sha512(text.strip().upper().encode()).hexdigest()


def del_old():
    posts = Post.objects.all()
    for post in posts:
        if post.need_delete():
            if os.path.isfile(post.path):
                os.remove(post.path)
            post.delete()


def index(request):
    del_old()
    return render(request, 'SpeechIT/homepage.html', {'path': request.path})


def to_speech(request):
    text_data = request.POST['qtext']
    text_lang = request.POST['lang']
    hash_digit = get_hash(text_data+text_lang)
    ip = get_ip(request)
    Post.objects.update_or_create(hash_str=hash_digit, defaults={'text': text_data, 'lang': text_lang,
                                                                 'ip': ip, 'date': timezone.now(),
                                                                 'path': os.path.join(settings.MEDIA_ROOT,
                                                                                      f'{hash_digit}.mp3')})
    return HttpResponseRedirect(reverse('SpeechIT:audio_page', args=(hash_digit,)))


def audio_page(request, hash_):
    from_db = Post.objects.get(hash_str=hash_)
    if not os.path.isfile(from_db.path):
        file = gTTS(text=from_db.text, lang=from_db.lang)
        file.save(from_db.path)

    return render(request, 'SpeechIT/download.html',
                  {'db': from_db, 'media': f"{settings.MEDIA_URL}{hash_}.mp3"})
