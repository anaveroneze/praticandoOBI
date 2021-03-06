from django.urls import path
from django.conf.urls import include, url
from usuarios.views import upload_drive, provaperson_baixar, provaperson_excluir, provaperson_baixar_docx, dadosbanco, update_perfil, cadastro_perfil, questoes_add, questoes_busca, home_usuario, provaperson, provaperson_detail, provaperson_edit, provasperson, provaperson_pronta
from provasobi.views import provas, problemas
from django.contrib.auth import views as auth_views

app_name = 'usuarios_obi'
urlpatterns = [
    path('', home_usuario, name='homeusuario'),
    path('cadastro/', cadastro_perfil, name='cadastro_perfil'),

    path('banco/', dadosbanco, name='dadosbanco'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login_perfil'),
    path('login/', include('registration.backends.default.urls')),
    path('logout/', auth_views.LogoutView.as_view(template_name='home.html'), name='logout_perfil'),
    path('novaprova/', provaperson, name='provaperson'),
    path('minhasprovas/', provasperson, name='provasperson'),
    path('minhasprovas/editar/<int:pk>/', provaperson_edit, name='provaperson_edit'),
    path('minhasprovas/editar/<int:pk>/buscaquestoes/', questoes_busca, name='questoes_busca'),
    path('minhasprovas/<int:pk>/', provaperson_detail, name='provaperson_detail'),

    path('minhasprovas/editar/<int:codprova>/adquestoes/<int:pk>/', questoes_add, name='questoes_add'),
    path('minhasprovas/<int:codprova>/verprova/', provaperson_pronta, name='provaperson_pronta'),
    path('minhasprovas/<int:codprova>/baixarprova/', provaperson_baixar, name='provaperson_baixar'),
    path('minhasprovas/excluir/<int:pk>/', provaperson_excluir, name='provaperson_excluir'),
    path('minhasprovas/<int:codprova>/baixarprova_docx/', provaperson_baixar_docx, name='provaperson_baixar_docx'),
    path('minhasprovas/<int:codprova>/upload_drive/', upload_drive, name='upload_drive'),

# path('minhasprovas/pdf/', Pdf.as_view(), name='provaperson_baixar'),
]