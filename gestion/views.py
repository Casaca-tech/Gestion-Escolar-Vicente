from django.shortcuts import render
from rest_framework import viewsets

from .models import (
    Perfil, Usuario, Recurso, Dependencia,
    Operacion, Estado, Historial, Indicador
)
from .serializer import (
    PerfilSerializer, UsuarioSerializer, RecursoSerializer,
    DependenciaSerializer, OperacionSerializer, EstadoSerializer,
    HistorialSerializer, IndicadorSerializer
)


def inicio(request):
    contexto = {
        'titulo': 'Bienvenido',
        'subtitulo': 'Sistema de Gestión Escolar',
        'descripcion': 'Plataforma integral para la gestión académica y administrativa de establecimientos educacionales.',
        'caracteristicas': [
            'Gestión centralizada de información',
            'Control de operaciones y estados',
            'Generación de indicadores de gestión',
            'Historial y auditoría de cambios'
        ]
    }
    return render(request, 'gestion/inicio.html', contexto)

# VISTA PERSONALIZADA PARA ERROR 404

def error_404(request, exception=None):
    return render(
        request,
        'gestion/404.html',
        {'mensaje': 'Recurso no encontrado'},
        status=404
    )


class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class RecursoViewSet(viewsets.ModelViewSet):
    queryset = Recurso.objects.all()
    serializer_class = RecursoSerializer


class DependenciaViewSet(viewsets.ModelViewSet):
    queryset = Dependencia.objects.all()
    serializer_class = DependenciaSerializer


class OperacionViewSet(viewsets.ModelViewSet):
    queryset = Operacion.objects.all()
    serializer_class = OperacionSerializer


class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer


class HistorialViewSet(viewsets.ModelViewSet):
    queryset = Historial.objects.all()
    serializer_class = HistorialSerializer


class IndicadorViewSet(viewsets.ModelViewSet):
    queryset = Indicador.objects.all()
    serializer_class = IndicadorSerializer