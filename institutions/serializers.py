from rest_framework import serializers

from institutions.models.institution import Institution


class InstitutionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'


class InstitutionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'