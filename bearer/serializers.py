from rest_framework import serializers
from bearer.models import Bearer


class BearerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bearer
        fields = '__all__'