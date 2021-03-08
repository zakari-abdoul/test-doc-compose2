from rest_framework import serializers
from globalP.models import Countries


class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = ['nom', 'alpha3Code', 'callingCodes', 'capital', 'region', 'flag']
