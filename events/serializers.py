# Serializers for events app

from rest_framework import serializers
from .models import Event, EventSeverity
from alerts.models import Alert
from logging import getLogger
logger = getLogger(__name__)

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        event = super().create(validated_data)
        logger.info(
            f"Event created | id={event.id} | severity={event.get_severity_display()}"
        )
        if event.severity in [EventSeverity.HIGH, EventSeverity.CRITICAL]:
            alert = Alert.objects.create(event=event)
            logger.warning(
                f"Alert auto-created | alert_id={alert.id} | event_id={event.id}"
            )
        return event

class EventDetailSerializer(serializers.ModelSerializer):
    severity = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'
    def get_severity(self, obj):
        return obj.get_severity_display()
