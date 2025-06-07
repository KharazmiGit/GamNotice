from django.db import models
from botbot.models import GamUser


class SummaryLetter(models.Model):
    user = models.ForeignKey(GamUser, on_delete=models.CASCADE, null=True, related_name='user_letter')
    sender = models.CharField(max_length=200)
    receiver = models.CharField(max_length=200)
    letter_id = models.CharField(max_length=10)
    sent_time = models.CharField(max_length=300)
    create_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} sent a letter to {self.receiver}"


class LetterArchive(models.Model):
    user = models.ForeignKey(GamUser, on_delete=models.CASCADE)
    letter_id = models.CharField(max_length=10, db_index=True)
    sent_time = models.CharField(max_length=300, db_index=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.letter_id} shipping time is {self.create_at}"
