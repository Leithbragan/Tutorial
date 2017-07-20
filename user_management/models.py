from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class SimpleUser(models.Model):
    class Meta:
        verbose_name = u'пользователь'
        verbose_name_plural = u'пользователи'
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=u'пользователь')
    second_name = models.CharField(max_length=40, verbose_name=u'фамилия')
    moder = models.BooleanField(default=False, verbose_name=u'модератор')

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.second_name)
