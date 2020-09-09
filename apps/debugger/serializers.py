from rest_framework import serializers
from .models import Debugger

class DebuggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debugger
        fields = '__all__'
