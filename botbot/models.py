from django.db import models
from django.contrib.auth.models import User


class GamUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='gam_user')
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    desktop_ip = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username
