import django_filters
from .models import Alert, AlertStatus
from events.models import EventSeverity

class AlertFilter(django_filters.FilterSet):
    status = django_filters.NumberFilter(field_name='status')
    severity = django_filters.NumberFilter(field_name='event__severity')