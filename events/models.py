from django.db import models

# Create your models here.
class EventSeverity(models.IntegerChoices):
    LOW = 1, 'Low'
    MEDIUM = 2, 'Medium'
    HIGH = 3, 'High'
    CRITICAL = 4, 'Critical'

class Event(models.Model):
    source = models.CharField(max_length=50)
    event_type = models.CharField(max_length=50)
    severity = models.PositiveIntegerField(choices=EventSeverity)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} - {self.get_severity_display()}"