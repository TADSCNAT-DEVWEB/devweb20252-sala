from rest_framework import serializers
from adocato.models import Raca, Gato
#from datetime import date


class RacaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(max_length=100, required=True)

    def validate_nome(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('O nome da raça deve ter pelo menos 3 caracteres.')
        return value

