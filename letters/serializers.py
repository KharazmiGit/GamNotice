from rest_framework import serializers
from .models import SummaryLetter


class SummaryLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryLetter
        fields = ['letter_id', 'sender', 'sent_time']
