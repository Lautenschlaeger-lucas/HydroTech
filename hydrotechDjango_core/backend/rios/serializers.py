from .models import Rios, PontoRisco
from rest_framework import serializers


class RiosSerializer(serializers.ModelSerializer):
    favorito = serializers.SerializerMethodField()
    criado_por = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Rios
        fields = '__all__'

    def get_favorito(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and getattr(user, 'is_authenticated', False):
            return user.favoritos.filter(pk=obj.pk).exists()
        return False


class PontoRiscoSerializer(serializers.ModelSerializer):
    criado_por_nome = serializers.CharField(source='criado_por.nome', read_only=True)
    rio_nome = serializers.CharField(source='rio.nome', read_only=True)
    
    class Meta:
        model = PontoRisco
        fields = ['id', 'rio', 'rio_nome', 'latitude', 'longitude', 'descricao', 'nivel_risco', 'criado_por', 'criado_por_nome', 'criado_em', 'atualizado_em']
        read_only_fields = ['criado_por', 'criado_em', 'atualizado_em']
