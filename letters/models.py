from django.db import models
from django.contrib.auth.models import User


class SummaryLetter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    sender = models.CharField(max_length=200)
    receiver = models.CharField(max_length=200)
    letter_id = models.CharField(max_length=10)
    sent_time = models.CharField(max_length=300)
    create_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} sent a letter to {self.receiver}"
