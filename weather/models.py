from django.db import models
from django.contrib.auth.models import User


class History(models.Model):
    user = models.ForeignKey(User, related_name='history', on_delete=models.CASCADE)
    city = models.CharField(max_length=20, verbose_name='Город')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время запроса')

    def __str__(self):
        return self.city