from rest_framework import serializers
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'asset', 'price', 'status', 'created']
        read_only_fields = ['status', 'created']

    def update(self, instance, validated_data):
        instance.modify_update_data(validated_data)
        return super().update(instance, validated_data)
