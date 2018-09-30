from django.urls import path
from usuarios.views import update_perfil, cadastro_perfil, questoes_add, home_usuario, provaperson, provaperson_detail, provaperson_edit, provasperson, problemas_add
from provasobi.views import provas, problemas
from django.contrib.auth import views as auth_views

app_name = 'usuarios_obi'
urlpatterns = [
    path('', home_usuario, name='homeusuario'),
    path('cadastro/', cadastro_perfil, name='cadastro_perfil'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login_perfil'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home.html'), name='logout_perfil'),
    path('nova/', provaperson, name='provaperson'),
    path('minhasprovas/', provasperson, name='provasperson'),
    path('minhasprovas/editar/<int:pk>', provaperson_edit, name='provaperson_edit'),
    path('minhasprovas/editar/<int:pk>/addquestoes', questoes_add, name='questoes_add'),
    path('minhasprovas/<int:pk>', provaperson_detail, name='provaperson_detail'),

    path('<int:pk>/addproblemas/<int:codprova>/', problemas_add, name='url_addprob'),
    #path('', update_perfil, name='update_perfil'),
]