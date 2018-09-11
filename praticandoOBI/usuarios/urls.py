from django.urls import path
from usuarios.views import update_perfil

app_name = 'usuarios_obi'
urlpatterns = [
    path('', update_perfil, name='update_perfil'),
]