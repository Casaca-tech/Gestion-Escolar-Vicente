from django.contrib import admin
from .models import (
    Perfil, Usuario, Recurso, Dependencia,
    Operacion, Estado, Historial, Indicador
)

admin.site.register(Perfil)
admin.site.register(Usuario)
admin.site.register(Recurso)
admin.site.register(Dependencia)
admin.site.register(Operacion)
admin.site.register(Estado)
admin.site.register(Historial)
admin.site.register(Indicador)