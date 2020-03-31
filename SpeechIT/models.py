from platform import version

from django.db import models
from django.utils import timezone
from datetime import timedelta


class Post(models.Model):
    text = models.TextField(verbose_name='Text')
    lang = models.CharField(verbose_name='language', max_length=2, default='ru')
    hash_str = models.CharField(verbose_name='hash', max_length=128, editable=None)
    ip = models.CharField(verbose_name='from IP', max_length=15)
    date = models.DateTimeField(verbose_name='post date', auto_now=True)
    path = models.TextField(verbose_name='path', editable=None, blank=True)

    def __str__(self):
        return self.text

    def need_delete(self):
        return self.date <= timezone.now() - timedelta(days=1)

    class Meta:
        verbose_name = 'Text'
        verbose_name_plural = 'Texts'

