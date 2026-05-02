from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, required=False, allow_blank=True)
    favoritos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'senha', 'data_criacao', 'data_nascimento', 'favoritos']
        read_only_fields = ['id', 'data_criacao', 'favoritos']

    def validate(self, attrs):
        if self.instance is None and not attrs.get('senha'):
            raise serializers.ValidationError({'senha': 'Senha é obrigatória.'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('senha')
        validated_data['senha'] = make_password(password)
        user = super().create(validated_data)
        if not user.token:
            user.token = user.generate_token()
            user.save(update_fields=['token'])
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('senha', None)
        if password:
            instance.senha = make_password(password)
        return super().update(instance, validated_data)
