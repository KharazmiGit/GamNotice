from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SummaryLetter
from .serializers import SummaryLetterSerializer

class UnreadLettersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = SummaryLetter.objects.filter(user=request.user, sent=False)
        ser = SummaryLetterSerializer(qs, many=True)
        qs.update(sent=True)
        return Response({'unread': ser.data})
