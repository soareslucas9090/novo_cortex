from django.urls import path, include

app_name = 'usuarios'

urlpatterns = [
    path('', include('Usuarios.usuarios.urls')),
    path('conta/', include('Usuarios.conta.urls')),
]
