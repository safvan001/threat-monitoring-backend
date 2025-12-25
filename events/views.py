from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer
from rest_framework.permissions import IsAdminUser


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]
