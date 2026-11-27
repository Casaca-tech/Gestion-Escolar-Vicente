from django.urls import path, include
from rest_framework import routers
from gestion import views

# API REST (ViewSets + Router)  ->  /gestion/perfiles/, etc.
enrutador = routers.DefaultRouter()

enrutador.register(r'perfiles', views.PerfilViewSet)
enrutador.register(r'usuarios', views.UsuarioViewSet)
enrutador.register(r'recursos', views.RecursoViewSet)
enrutador.register(r'dependencias', views.DependenciaViewSet)
enrutador.register(r'operaciones', views.OperacionViewSet)
enrutador.register(r'estados', views.EstadoViewSet)
enrutador.register(r'historial', views.HistorialViewSet)
enrutador.register(r'indicadores', views.IndicadorViewSet)


# CRUD WEB (CBV)  ->  /gestion/web/perfiles/, etc.
def rutas_crud(base, nombre, lista, detalle, crear, editar, eliminar):
    """Registra las 5 rutas CRUD de una entidad."""
    return [
        path(f'web/{base}/', lista.as_view(), name=f'{nombre}_list'),
        path(f'web/{base}/nuevo/', crear.as_view(), name=f'{nombre}_create'),
        path(f'web/{base}/<int:pk>/', detalle.as_view(), name=f'{nombre}_detail'),
        path(f'web/{base}/<int:pk>/editar/', editar.as_view(), name=f'{nombre}_update'),
        path(f'web/{base}/<int:pk>/eliminar/', eliminar.as_view(), name=f'{nombre}_delete'),
    ]


urlpatterns = (
    rutas_crud('perfiles', 'perfil', views.PerfilListView, views.PerfilDetailView,
               views.PerfilCreateView, views.PerfilUpdateView, views.PerfilDeleteView)
    + rutas_crud('usuarios', 'usuario', views.UsuarioListView, views.UsuarioDetailView,
                 views.UsuarioCreateView, views.UsuarioUpdateView, views.UsuarioDeleteView)
    + rutas_crud('recursos', 'recurso', views.RecursoListView, views.RecursoDetailView,
                 views.RecursoCreateView, views.RecursoUpdateView, views.RecursoDeleteView)
    + rutas_crud('dependencias', 'dependencia', views.DependenciaListView, views.DependenciaDetailView,
                 views.DependenciaCreateView, views.DependenciaUpdateView, views.DependenciaDeleteView)
    + rutas_crud('operaciones', 'operacion', views.OperacionListView, views.OperacionDetailView,
                 views.OperacionCreateView, views.OperacionUpdateView, views.OperacionDeleteView)
    + rutas_crud('estados', 'estado', views.EstadoListView, views.EstadoDetailView,
                 views.EstadoCreateView, views.EstadoUpdateView, views.EstadoDeleteView)
    + rutas_crud('historial', 'historial', views.HistorialListView, views.HistorialDetailView,
                 views.HistorialCreateView, views.HistorialUpdateView, views.HistorialDeleteView)
    + rutas_crud('indicadores', 'indicador', views.IndicadorListView, views.IndicadorDetailView,
                 views.IndicadorCreateView, views.IndicadorUpdateView, views.IndicadorDeleteView)
    + [path('', include(enrutador.urls))]
)
