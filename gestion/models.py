from django.db import models

# ============================================================
# CONSTANTES REUTILIZABLES
# ============================================================
int_habilitado = 1
str_fecha_creacion = "Fecha Creación"
str_fecha_actualizacion = "Fecha Actualización"
str_codigo = "Código"
str_nombre = "Nombre"
str_descripcion = "Descripción"
str_email = "Email"


# ============================================================
# 1. PERFIL
# ============================================================
class Perfil(models.Model):
    nombre = models.CharField("Nombre", max_length=50, unique=True, null=False)
    descripcion = models.CharField(str_descripcion, max_length=255, null=True)
    es_publico = models.BooleanField("Es Público", default=False, null=False)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    def __str__(self):
        return self.nombre


# ============================================================
# 2. USUARIO
# ============================================================
class Usuario(models.Model):
    nombre = models.CharField(str_nombre, max_length=150, null=False)

    correo = models.EmailField(str_email, max_length=191, unique=True, null=False)

    contrasenia = models.CharField("Contraseña", max_length=128, null=False)
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT, null=False)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    def __str__(self):
        return self.nombre


# ============================================================
# 3. RECURSO
# ============================================================
class Recurso(models.Model):
    codigo = models.CharField(str_codigo, max_length=20, unique=True, null=False)
    nombre = models.CharField(str_nombre, max_length=100, null=False)
    descripcion = models.CharField(str_descripcion, max_length=255, null=True)
    tipo = models.CharField("Tipo", max_length=50, null=False)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


# ============================================================
# 4. DEPENDENCIA
# ============================================================
class Dependencia(models.Model):
    origen = models.ForeignKey(
        Recurso, on_delete=models.CASCADE,
        related_name='dependencias_origen', null=False
    )
    destino = models.ForeignKey(
        Recurso, on_delete=models.CASCADE,
        related_name='dependencias_destino', null=False
    )
    tipo = models.CharField("Tipo", max_length=50, null=False)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    def __str__(self):
        return f"{self.origen} -> {self.destino} ({self.tipo})"


# ============================================================
# 5. OPERACION
# ============================================================
class Operacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False)
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, null=False)
    tipo = models.CharField("Tipo", max_length=50, null=False)
    fecha = models.DateTimeField("Fecha", auto_now_add=True)
    detalle = models.TextField("Detalle", null=True)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)

    def __str__(self):
        return f"{self.usuario} - {self.tipo} - {self.recurso}"


# ============================================================
# 6. ESTADO
# ============================================================
class Estado(models.Model):
    nombre = models.CharField(str_nombre, max_length=50, null=False)
    descripcion = models.CharField(str_descripcion, max_length=255, null=True)
    es_excepcional = models.BooleanField("Es Excepcional", default=False, null=False)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    def __str__(self):
        return self.nombre


# ============================================================
# 7. HISTORIAL
# ============================================================
class Historial(models.Model):
    operacion = models.ForeignKey(Operacion, on_delete=models.CASCADE, null=False)
    estado_anterior = models.ForeignKey(
        Estado, on_delete=models.SET_NULL,
        null=True, related_name='historial_anterior'
    )
    estado_nuevo = models.ForeignKey(
        Estado, on_delete=models.SET_NULL,
        null=True, related_name='historial_nuevo'
    )
    fecha = models.DateTimeField("Fecha", auto_now_add=True)
    observacion = models.TextField("Observación", null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Historial {self.id} - {self.fecha}"


# ============================================================
# 8. INDICADOR
# ============================================================
class Indicador(models.Model):
    nombre = models.CharField(str_nombre, max_length=100, null=False)
    descripcion = models.CharField(str_descripcion, max_length=255, null=True)
    formula = models.TextField("Fórmula", null=True)
    periodo = models.CharField("Período", max_length=50, null=False)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    def __str__(self):
        return self.nombre