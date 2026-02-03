from rest_framework import serializers
from adocato.models import Raca, Gato
from datetime import date


class RacaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(max_length=100, required=True)

    def validate_nome(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('O nome da raça deve ter pelo menos 3 caracteres.')
        return value


class GatoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(max_length=100, required=True)
    sexo = serializers.ChoiceField(choices=[('M', 'Macho'), ('F', 'Femea')], required=True)
    cor = serializers.CharField(max_length=50, required=True)
    data_nascimento = serializers.DateField(required=True)
    descricao = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    disponivel = serializers.BooleanField(default=True)
    raca_id = serializers.IntegerField(write_only=True, required=True)
    raca = RacaSerializer(read_only=True)
    foto = serializers.ImageField(required=False, allow_null=True, use_url=False)
    foto_url = serializers.SerializerMethodField()
    idade = serializers.IntegerField(read_only=True)
    
    def get_foto_url(self, obj):
        if obj.foto:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto.url)
            return obj.foto.url
        return None

    def validate_nome(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('O nome do gato deve ter pelo menos 5 caracteres.')
        return value

    def validate_cor(self, value):
        if not value:
            raise serializers.ValidationError('A cor do gato é obrigatória.')
        return value

    def validate_sexo(self, value):
        if value not in ['M', 'F']:
            raise serializers.ValidationError('O sexo deve ser "M" para macho ou "F" para fêmea.')
        return value

    def validate_data_nascimento(self, value):
        if not value:
            raise serializers.ValidationError('A data de nascimento é obrigatória.')
        if value > date.today():
            raise serializers.ValidationError('A data de nascimento não pode ser no futuro.')
        return value
