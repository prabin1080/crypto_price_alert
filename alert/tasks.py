from celery import shared_task
from .models import Alert


@shared_task
def initialize_new_records(current_prices):
    Alert.objects.set_track_type(current_prices)


@shared_task
def process_record(alert_id):
    alert = Alert.objects.get(id=alert_id)
    alert.set_triggered()
    print(f'Price {alert.price} has reached for alert {alert.id} and user {alert.user.id}')


@shared_task
def process_records(current_prices):
    initialize_new_records.delay(current_prices)
    for alert in Alert.objects.get_alert_eligible_queryset(current_prices):
        process_record.delay(alert.id)
