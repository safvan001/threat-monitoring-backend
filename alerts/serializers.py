# Serializers for alerts app

from rest_framework import serializers
from .models import Alert
from events.serializers import EventDetailSerializer
from logging import getLogger
logger = getLogger(__name__)

class AlertSerializer(serializers.ModelSerializer):
    event = EventDetailSerializer(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Alert
        fields = '__all__'
    def get_status(self, obj):
        return obj.get_status_display()

class AlertUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['status']

    def update(self, instance, validated_data):
        old_status = instance.get_status_display()
        updated_instance = super().update(instance, validated_data)
        new_status = updated_instance.get_status_display()
        logger.info(
            f"Alert status updated | alert_id={instance.id} | old_status={old_status} | new_status={new_status}"
        )
        return updated_instance
