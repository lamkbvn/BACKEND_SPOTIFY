from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from ..common.models import LichSuNghe
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def top_songs(request):
    top_songs = LichSuNghe.objects.filter(
        thoi_gian_nghe__gte='2025-03-01'
    ).values('bai_hat').annotate(luot_nghe=Count('bai_hat')).order_by('-luot_nghe')[:10]
    return Response(top_songs)