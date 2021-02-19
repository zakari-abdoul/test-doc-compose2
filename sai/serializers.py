from rest_framework import serializers
from sai.models import Sai_IN, Sai_OUT


class Sai_IN_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sai_IN
        fields = '__all__'


class Sai_OUT_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sai_OUT
        fields = '__all__'


class Sai_OUT_Post_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sai_OUT
        fields = ['Interval_Time','Opcode',]


class FileSaiSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    inputFile = serializers.FileField(max_length=None, required=True)