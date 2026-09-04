from django.shortcuts import render

class Custom404Middleware:
    """
    Middleware para manejar errores 404 incluso cuando DEBUG=True
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Si la respuesta es 404 y estamos en DEBUG, mostrar página personalizada
        if response.status_code == 404 and request.path != '/admin/':
            # Verificar si la página es para admin
            if not request.path.startswith('/admin/'):
                # Redirigir a nuestra vista de error 404
                from django.template import loader
                from django.http import HttpResponseNotFound
                from django.template import TemplateDoesNotExist
                
                try:
                    template = loader.get_template('gestion/404.html')
                    context = {'mensaje': 'Recurso no encontrado'}
                    return HttpResponseNotFound(template.render(context, request))
                except TemplateDoesNotExist:
                    # Si el template no existe, usar el error estándar
                    pass
                
        return response