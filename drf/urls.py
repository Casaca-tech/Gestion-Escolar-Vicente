from django.contrib import admin
from django.urls import path, include
from gestion import views

handler404 = 'gestion.views.error_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('gestion/', include('gestion.urls')),
]