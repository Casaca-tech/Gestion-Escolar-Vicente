from rest_framework import serializers

from .models import (
    Perfil, Usuario, Recurso, Dependencia,
    Operacion, Estado, Historial, Indicador
)


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ('__all__')


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('__all__')


class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = ('__all__')


class DependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependencia
        fields = ('__all__')


class OperacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operacion
        fields = ('__all__')


class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ('__all__')


class HistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historial
        fields = ('__all__')


class IndicadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicador
        fields = ('__all__')