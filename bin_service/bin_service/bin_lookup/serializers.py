from rest_framework import serializers
from .models import BinInfo

class BinInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinInfo
        fields = ['bin_number', 'bank_name']
