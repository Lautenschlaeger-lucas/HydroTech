from .models import Rios
from rest_framework import serializers

class RiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rios
        fields = '__all__'

        