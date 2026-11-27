from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from rest_framework import viewsets

from .forms import (
    PerfilForm, UsuarioForm, RecursoForm, DependenciaForm,
    OperacionForm, EstadoForm, HistorialForm, IndicadorForm
)
from .models import (
    Perfil, Usuario, Recurso, Dependencia,
    Operacion, Estado, Historial, Indicador
)
from .serializer import (
    PerfilSerializer, UsuarioSerializer, RecursoSerializer,
    DependenciaSerializer, OperacionSerializer, EstadoSerializer,
    HistorialSerializer, IndicadorSerializer
)


# ============================================================
# VISTA PUBLICA DE BIENVENIDA
# ============================================================
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
        ],
        'modulos': [
            ('Perfiles', 'perfil_list'),
            ('Usuarios', 'usuario_list'),
            ('Recursos', 'recurso_list'),
            ('Dependencias', 'dependencia_list'),
            ('Operaciones', 'operacion_list'),
            ('Estados', 'estado_list'),
            ('Historial', 'historial_list'),
            ('Indicadores', 'indicador_list'),
        ],
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


# ============================================================
# API REST (ViewSets)
# ============================================================
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


# ============================================================
# CRUD WEB CON VISTAS BASADAS EN CLASES (CBV)
# ============================================================
def _fmt(valor):
    """Formatea valores para mostrarlos en las plantillas."""
    if valor is True:
        return 'Sí'
    if valor is False:
        return 'No'
    if valor is None or valor == '':
        return '—'
    return valor


class CrudMixin:
    """Datos comunes de cada entidad y redirección posterior a la operación."""
    entidad = ''
    titulo = ''
    singular = ''
    columnas = []
    excluir = []

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'entidad': self.entidad,
            'titulo': self.titulo,
            'singular': self.singular,
        })
        return ctx

    def get_success_url(self):
        return reverse(f'{self.entidad}_list')


class CrudListView(CrudMixin, ListView):
    template_name = 'gestion/crud/lista.html'
    paginate_by = 10
    ordering = ['id']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        campos = [self.model._meta.get_field(c) for c in self.columnas]
        ctx['encabezados'] = [str(c.verbose_name) for c in campos]
        ctx['filas'] = [
            (obj, [_fmt(getattr(obj, c.name)) for c in campos])
            for obj in ctx['page_obj']
        ]
        return ctx


class CrudDetailView(CrudMixin, DetailView):
    template_name = 'gestion/crud/detalle.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['campos'] = [
            (str(f.verbose_name), _fmt(getattr(self.object, f.name)))
            for f in self.model._meta.fields
            if f.name != 'id' and f.name not in self.excluir
        ]
        return ctx


class CrudCreateView(CrudMixin, SuccessMessageMixin, CreateView):
    template_name = 'gestion/crud/formulario.html'
    success_message = 'Registro creado correctamente.'


class CrudUpdateView(CrudMixin, SuccessMessageMixin, UpdateView):
    template_name = 'gestion/crud/formulario.html'
    success_message = 'Registro actualizado correctamente.'


class CrudDeleteView(CrudMixin, DeleteView):
    template_name = 'gestion/crud/confirmar_eliminar.html'

    def form_valid(self, form):
        try:
            respuesta = super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                'No se puede eliminar: el registro está siendo usado por otros registros.'
            )
            return redirect(reverse(f'{self.entidad}_detail', args=[self.object.pk]))
        messages.success(self.request, 'Registro eliminado correctamente.')
        return respuesta


# ---------- PERFIL ----------
class PerfilConfig:
    model = Perfil
    form_class = PerfilForm
    entidad, titulo, singular = 'perfil', 'Perfiles', 'Perfil'
    columnas = ['nombre', 'descripcion', 'es_publico', 'habilitado']

class PerfilListView(PerfilConfig, CrudListView): pass
class PerfilDetailView(PerfilConfig, CrudDetailView): pass
class PerfilCreateView(PerfilConfig, CrudCreateView): pass
class PerfilUpdateView(PerfilConfig, CrudUpdateView): pass
class PerfilDeleteView(PerfilConfig, CrudDeleteView): pass


# ---------- USUARIO ----------
class UsuarioConfig:
    model = Usuario
    form_class = UsuarioForm
    entidad, titulo, singular = 'usuario', 'Usuarios', 'Usuario'
    columnas = ['nombre', 'correo', 'perfil', 'habilitado']
    excluir = ['contrasenia']

class UsuarioListView(UsuarioConfig, CrudListView): pass
class UsuarioDetailView(UsuarioConfig, CrudDetailView): pass
class UsuarioCreateView(UsuarioConfig, CrudCreateView): pass
class UsuarioUpdateView(UsuarioConfig, CrudUpdateView): pass
class UsuarioDeleteView(UsuarioConfig, CrudDeleteView): pass


# ---------- RECURSO ----------
class RecursoConfig:
    model = Recurso
    form_class = RecursoForm
    entidad, titulo, singular = 'recurso', 'Recursos', 'Recurso'
    columnas = ['codigo', 'nombre', 'tipo', 'habilitado']

class RecursoListView(RecursoConfig, CrudListView): pass
class RecursoDetailView(RecursoConfig, CrudDetailView): pass
class RecursoCreateView(RecursoConfig, CrudCreateView): pass
class RecursoUpdateView(RecursoConfig, CrudUpdateView): pass
class RecursoDeleteView(RecursoConfig, CrudDeleteView): pass


# ---------- DEPENDENCIA ----------
class DependenciaConfig:
    model = Dependencia
    form_class = DependenciaForm
    entidad, titulo, singular = 'dependencia', 'Dependencias', 'Dependencia'
    columnas = ['origen', 'destino', 'tipo', 'habilitado']

class DependenciaListView(DependenciaConfig, CrudListView): pass
class DependenciaDetailView(DependenciaConfig, CrudDetailView): pass
class DependenciaCreateView(DependenciaConfig, CrudCreateView): pass
class DependenciaUpdateView(DependenciaConfig, CrudUpdateView): pass
class DependenciaDeleteView(DependenciaConfig, CrudDeleteView): pass


# ---------- OPERACION ----------
class OperacionConfig:
    model = Operacion
    form_class = OperacionForm
    entidad, titulo, singular = 'operacion', 'Operaciones', 'Operación'
    columnas = ['usuario', 'recurso', 'tipo', 'fecha']

class OperacionListView(OperacionConfig, CrudListView): pass
class OperacionDetailView(OperacionConfig, CrudDetailView): pass
class OperacionCreateView(OperacionConfig, CrudCreateView): pass
class OperacionUpdateView(OperacionConfig, CrudUpdateView): pass
class OperacionDeleteView(OperacionConfig, CrudDeleteView): pass


# ---------- ESTADO ----------
class EstadoConfig:
    model = Estado
    form_class = EstadoForm
    entidad, titulo, singular = 'estado', 'Estados', 'Estado'
    columnas = ['nombre', 'descripcion', 'es_excepcional', 'habilitado']

class EstadoListView(EstadoConfig, CrudListView): pass
class EstadoDetailView(EstadoConfig, CrudDetailView): pass
class EstadoCreateView(EstadoConfig, CrudCreateView): pass
class EstadoUpdateView(EstadoConfig, CrudUpdateView): pass
class EstadoDeleteView(EstadoConfig, CrudDeleteView): pass


# ---------- HISTORIAL ----------
class HistorialConfig:
    model = Historial
    form_class = HistorialForm
    entidad, titulo, singular = 'historial', 'Historial', 'Registro de historial'
    columnas = ['operacion', 'estado_anterior', 'estado_nuevo', 'fecha']

class HistorialListView(HistorialConfig, CrudListView): pass
class HistorialDetailView(HistorialConfig, CrudDetailView): pass
class HistorialCreateView(HistorialConfig, CrudCreateView): pass
class HistorialUpdateView(HistorialConfig, CrudUpdateView): pass
class HistorialDeleteView(HistorialConfig, CrudDeleteView): pass


# ---------- INDICADOR ----------
class IndicadorConfig:
    model = Indicador
    form_class = IndicadorForm
    entidad, titulo, singular = 'indicador', 'Indicadores', 'Indicador'
    columnas = ['nombre', 'periodo', 'habilitado']

class IndicadorListView(IndicadorConfig, CrudListView): pass
class IndicadorDetailView(IndicadorConfig, CrudDetailView): pass
class IndicadorCreateView(IndicadorConfig, CrudCreateView): pass
class IndicadorUpdateView(IndicadorConfig, CrudUpdateView): pass
class IndicadorDeleteView(IndicadorConfig, CrudDeleteView): pass
