from django.urls import path, include
from rest_framework import routers
from gestion import views

# Enrutador que genera automáticamente las rutas para los ViewSets
enrutador = routers.DefaultRouter()

enrutador.register(r'perfiles', views.PerfilViewSet)
enrutador.register(r'usuarios', views.UsuarioViewSet)
enrutador.register(r'recursos', views.RecursoViewSet)
enrutador.register(r'dependencias', views.DependenciaViewSet)
enrutador.register(r'operaciones', views.OperacionViewSet)
enrutador.register(r'estados', views.EstadoViewSet)
enrutador.register(r'historial', views.HistorialViewSet)
enrutador.register(r'indicadores', views.IndicadorViewSet)

urlpatterns = [
    path('', include(enrutador.urls)),
]