"""obi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from provasobi.views import home, provas, problemas, provaperson, provaperson_detail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('provas/', include('provasobi.urls', namespace='provas_obi')),
    path('admin/', admin.site.urls),
    path('usuario/', include('usuarios.urls', namespace='usuarios_obi')),

    #path('<int:pk>/minhasprovas/', minhasprovas, name='url_minhasprovas'),
    path('nova/', provaperson, name='provaperson'),
    path('nova/<int:pk>', provaperson_detail, name='provaperson_detail'),
   # path('prova/<int:pk>', provaperson_detail, name='provadetail'),
   # path('gabarito/<int:pk>', gabarito, name='url_gabarito'),
]
