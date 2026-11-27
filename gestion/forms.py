from django import forms
from django.contrib.auth.hashers import make_password

from .models import (
    Perfil, Usuario, Recurso, Dependencia,
    Operacion, Estado, Historial, Indicador
)

CTRL = 'form-control'
SELECT = 'form-select'
CHECK = 'form-check-input'


class OpcionalesMixin:
    """Marca como no obligatorios los campos listados en campos_opcionales."""
    campos_opcionales = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nombre in self.campos_opcionales:
            self.fields[nombre].required = False


class PerfilForm(OpcionalesMixin, forms.ModelForm):
    campos_opcionales = ['descripcion']

    class Meta:
        model = Perfil
        fields = ['nombre', 'descripcion', 'es_publico', 'habilitado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': CTRL, 'placeholder': 'Ej: Administrador'}),
            'descripcion': forms.Textarea(attrs={'class': CTRL, 'placeholder': 'Describa el perfil', 'rows': 3}),
            'es_publico': forms.CheckboxInput(attrs={'class': CHECK}),
            'habilitado': forms.CheckboxInput(attrs={'class': CHECK}),
        }


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'contrasenia', 'perfil', 'habilitado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': CTRL, 'placeholder': 'Nombre completo'}),
            'correo': forms.EmailInput(attrs={'class': CTRL, 'placeholder': 'correo@ejemplo.cl'}),
            'contrasenia': forms.PasswordInput(
                render_value=False,
                attrs={'class': CTRL, 'placeholder': 'Contraseña'}),
            'perfil': forms.Select(attrs={'class': SELECT}),
            'habilitado': forms.CheckboxInput(attrs={'class': CHECK}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['contrasenia'].required = False
            self.fields['contrasenia'].help_text = 'Déjela vacía para mantener la contraseña actual.'

    def clean_contrasenia(self):
        valor = self.cleaned_data.get('contrasenia')
        if self.instance.pk and not valor:
            return self.instance.contrasenia
        return make_password(valor)


class RecursoForm(OpcionalesMixin, forms.ModelForm):
    campos_opcionales = ['descripcion']

    class Meta:
        model = Recurso
        fields = ['codigo', 'nombre', 'descripcion', 'tipo', 'habilitado']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': CTRL, 'placeholder': 'Ej: REC-001'}),
            'nombre': forms.TextInput(attrs={'class': CTRL, 'placeholder': 'Nombre del recurso'}),
            'descripcion': forms.Textarea(attrs={'class': CTRL, 'placeholder': 'Descripción', 'rows': 3}),
            'tipo': forms.TextInput(attrs={'class': CTRL, 'placeholder': 'Ej: Sala, Equipo'}),
            'habilitado': forms.CheckboxInput(attrs={'class': CHECK}),
        }


class DependenciaForm(forms.ModelForm):
    class Meta:
        model = Dependencia
        fields = ['origen', 'destino', 'tipo', 'habilitado']
        widgets = {
            'origen': forms.Select(attrs={'class': SELECT}),
            'destino': forms.Select(attrs={'class': SELECT}),
            'tipo': forms.TextInput(attrs={'class': CTRL, 'placeholder': 'Tipo de dependencia'}),
            'habilitado': forms.CheckboxInput(attrs={'class': CHECK}),
        }


class OperacionForm(OpcionalesMixin, forms.ModelForm):
    campos_opcionales = ['detalle']

    class Meta:
        model = Operacion
        fields = ['usuario', 'recurso', 'tipo', 'detalle', 'habilitado']
        widgets = {
            'usuario': forms.Select(attrs={'class': SELECT}),
            'recurso': forms.Select(attrs={'class': SELECT}),
            'tipo': forms.TextInput(attrs={'class': CTRL, 'placeholder': 'Ej: Préstamo'}),
            'detalle': forms.Textarea(attrs={'class': CTRL, 'placeholder': 'Detalle de la operación', 'rows': 4}),
            'habilitado': forms.CheckboxInput(attrs={'class': CHECK}),
        }


class EstadoForm(OpcionalesMixin, forms.ModelForm):
    campos_opcionales = ['descripcion']

    class Meta:
        model = Estado
        fields = ['nombre', 'descripcion', 'es_excepcional', 'habilitado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': CTRL, 'placeholder': 'Ej: Activo'}),
            'descripcion': forms.Textarea(attrs={'class': CTRL, 'placeholder': 'Descripción del estado', 'rows': 3}),
            'es_excepcional': forms.CheckboxInput(attrs={'class': CHECK}),
            'habilitado': forms.CheckboxInput(attrs={'class': CHECK}),
        }


class HistorialForm(OpcionalesMixin, forms.ModelForm):
    campos_opcionales = ['estado_anterior', 'estado_nuevo', 'observacion', 'usuario']

    class Meta:
        model = Historial
        fields = ['operacion', 'estado_anterior', 'estado_nuevo', 'observacion', 'usuario']
        widgets = {
            'operacion': forms.Select(attrs={'class': SELECT}),
            'estado_anterior': forms.Select(attrs={'class': SELECT}),
            'estado_nuevo': forms.Select(attrs={'class': SELECT}),
            'observacion': forms.Textarea(attrs={'class': CTRL, 'placeholder': 'Observación', 'rows': 4}),
            'usuario': forms.Select(attrs={'class': SELECT}),
        }


class IndicadorForm(OpcionalesMixin, forms.ModelForm):
    campos_opcionales = ['descripcion', 'formula']

    class Meta:
        model = Indicador
        fields = ['nombre', 'descripcion', 'formula', 'periodo', 'habilitado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': CTRL, 'placeholder': 'Nombre del indicador'}),
            'descripcion': forms.Textarea(attrs={'class': CTRL, 'placeholder': 'Descripción', 'rows': 3}),
            'formula': forms.Textarea(attrs={'class': CTRL, 'placeholder': '(a / b) * 100', 'rows': 3}),
            'periodo': forms.TextInput(attrs={'class': CTRL, 'placeholder': 'Ej: Mensual'}),
            'habilitado': forms.CheckboxInput(attrs={'class': CHECK}),
        }
