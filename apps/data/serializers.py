from rest_framework import serializers
from apps.data.models import KeyVal


class KeyValStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyVal
        fields = ('pk', 'key', 'value',)
