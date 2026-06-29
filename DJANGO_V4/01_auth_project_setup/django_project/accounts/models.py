from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomerUser(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True, verbose_name='닉네임')
    def __str__(self):
        return self.username