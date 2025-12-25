from django.db import models
from events.models import Event
# Create your models here.

class AlertStatus(models.IntegerChoices):
    OPEN = 1, 'Open'
    ACKNOWLEDGED = 2, 'Acknowledged'
    RESOLVED = 3, 'Resolved'

class Alert(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(choices=AlertStatus,default=AlertStatus.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_status_display()} - {self.event}"