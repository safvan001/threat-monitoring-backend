from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Alert
from .serializers import AlertSerializer, AlertUpdateSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .filters import AlertFilter

class AlertListView(generics.ListAPIView):
    queryset = Alert.objects.select_related('event')
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = AlertFilter

class AlertUpdateView(generics.UpdateAPIView):
    queryset = Alert.objects.select_related('event')
    serializer_class = AlertUpdateSerializer
    permission_classes = [IsAdminUser]
    
