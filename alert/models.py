from django.db import models

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from functools import reduce
from operator import or_


class AlertManager(models.Manager):
    TRACK_UNKNOWN = 0
    TRACK_HIGH = 1
    TRACK_LOW = 2

    @staticmethod
    def filter_higher_prices(queryset: models.QuerySet, current_prices: dict) -> models.QuerySet:
        return queryset.filter(
            reduce(or_, [Q(asset=asset, price__gte=current_price) for asset, current_price in current_prices.items()])
        )

    @staticmethod
    def filter_lower_prices(queryset: models.QuerySet, current_prices: dict) -> models.QuerySet:
        return queryset.filter(
            reduce(or_, [Q(asset=asset, price__lte=current_price) for asset, current_price in current_prices.items()])
        )

    def get_alert_eligible_queryset(self, current_prices: dict) -> models.QuerySet:
        return super().get_queryset().filter(
            Q(status='CREATED'),
            reduce(
                or_,
                [
                    Q(asset=asset, track_type=self.TRACK_HIGH, price__lte=current_price) |
                    Q(asset=asset, track_type=self.TRACK_LOW, price__gte=current_price)
                    for asset, current_price in current_prices.items()
                ]
            )
        )

    def set_track_type(self, prices: dict):
        queryset = super().get_queryset().filter(
            Q(status='CREATED'),
            Q(track_type=self.TRACK_UNKNOWN)
        )
        self.filter_higher_prices(queryset, prices).update(track_type=self.TRACK_HIGH)
        self.filter_lower_prices(queryset, prices).update(track_type=self.TRACK_LOW)


class Alert(models.Model):
    # TRACK TYPE FOR PRICE LOW OR HIGH
    TRACK_UNKNOWN = 0
    TRACK_HIGH = 1
    TRACK_LOW = 2
    TRACK_TYPE_CHOICES = [
        (TRACK_UNKNOWN, 'TRACK_UNKNOWN'), (TRACK_HIGH, 'TRACK_HIGH'), (TRACK_LOW, 'TRACK_LOW'),
    ]

    # ASSET
    ASSET_CHOICES = [(asset, asset) for asset in settings.ASSETS]

    # STATUS
    CREATED = 'CREATED'
    DELETED = 'DELETED'
    TRIGGERED = 'TRIGGERED'
    STATUS_CHOICES = [
        (CREATED, 'CREATED'), (DELETED, 'DELETED'), (TRIGGERED, 'TRIGGERED'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.CharField(max_length=15, choices=ASSET_CHOICES)
    price = models.FloatField()
    track_type = models.IntegerField(choices=TRACK_TYPE_CHOICES, default=TRACK_UNKNOWN)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=CREATED)
    triggered_at = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = AlertManager()

    def __str__(self):
        return f'{self.asset}, {self.price}, {self.get_track_type_display()}, {self.status}'

    def modify_update_data(self, validated_data):
        if validated_data.get('price') and not validated_data.get('price') == getattr(self, 'price'):
            validated_data['track_type'] = self.TRACK_UNKNOWN
        if validated_data.get('asset') and not validated_data.get('asset') == getattr(self, 'asset'):
            validated_data['track_type'] = self.TRACK_UNKNOWN

    def soft_delete(self):
        self.status = self.DELETED
        self.save()

    def set_triggered(self):
        self.status = self.TRIGGERED
        self.triggered_at = timezone.now()
        self.save()
