from django.urls import path
from usuarios.views import entrar_perfil, provaperson_lista, provaperson_info, provaperson_nova

app_name = 'usuarios_obi'
urlpatterns = [
    path('', entrar_perfil, name='entrar_perfil'),
    path('minhasprovas', provaperson_lista, name='provaperson_lista'),
    path('minhasprovas/<int:pk>/', provaperson_info, name='provaperson_info'),
    path('minhasprovas/nova/', provaperson_nova, name='provaperson_nova'),
]