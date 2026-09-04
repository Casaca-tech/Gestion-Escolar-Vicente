from django.shortcuts import render

# Vista para la página de inicio
def inicio(request):
    contexto = {
        'titulo': 'Bienvenido',
        'subtitulo': 'Sistema de Gestión Escolar ',
        'descripcion': 'Plataforma integral para la gestión académica y administrativa de establecimientos educacionales.',
        'caracteristicas': [
            'Gestión de alumnos y docentes',
            'Control de asistencia y calificaciones',
            'Generación de reportes e indicadores',
            'Administración de cursos y asignaturas'
        ]
    }
    return render(request, 'gestion/inicio.html', contexto)

# Vista personalizada para error 404
def error_404(request, exception=None):
    return render(request, 'gestion/404.html', {'mensaje': 'Recurso no encontrado'}, status=404)