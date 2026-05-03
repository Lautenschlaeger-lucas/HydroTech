from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, required=False, allow_blank=True, min_length=8)
    favoritos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'senha', 'data_criacao', 'data_nascimento', 'is_defesa_civil', 'favoritos']
        read_only_fields = ['id', 'data_criacao', 'favoritos', 'api_token']

    def validate_nome(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError('Nome deve ter no mínimo 3 caracteres.')
        return value.strip()

    def validate_email(self, value):
        value = value.lower().strip()
        if self.instance is None:
            if Usuario.objects.filter(email=value).exists():
                raise serializers.ValidationError('Este email já está registrado.')
        else:
            if Usuario.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError('Este email já está registrado.')
        return value

    def validate_data_nascimento(self, value):
        today = timezone.now().date()
        age = (today - value).days // 365
        if age < 13:
            raise serializers.ValidationError('Você deve ter no mínimo 13 anos.')
        if value > today:
            raise serializers.ValidationError('Data de nascimento não pode ser no futuro.')
        return value

    def validate_senha(self, value):
        if not value:
            return value
        
        if len(value) < 8:
            raise serializers.ValidationError('Senha deve ter no mínimo 8 caracteres.')
        
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError('Senha deve conter pelo menos um número.')
        
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError('Senha deve conter pelo menos uma letra maiúscula.')
        
        if not any(char.islower() for char in value):
            raise serializers.ValidationError('Senha deve conter pelo menos uma letra minúscula.')
        
        return value

    def validate(self, attrs):
        if self.instance is None and not attrs.get('senha'):
            raise serializers.ValidationError({'senha': 'Senha é obrigatória.'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('senha', None)
        user = super().create(validated_data)
        
        if password:
            user.set_password(password)
        
        if not user.token:
            user.token = user.generate_token()
        
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('senha', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

