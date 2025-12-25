from django.urls import path
from events import views

app_name = "events"

urlpatterns = [
    path('create-event/', views.EventCreateView.as_view(), name='create-event'),
]


