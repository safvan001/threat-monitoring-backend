from django.urls import path
from alerts import views

app_name = "alerts"

urlpatterns = [
    path('list-alerts/', views.AlertListView.as_view(), name='list-alerts'),
    path('update-alert/<int:pk>/', views.AlertUpdateView.as_view(), name='update-alert'),
]


