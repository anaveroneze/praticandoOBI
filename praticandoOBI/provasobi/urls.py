from django.urls import path
from provasobi.views import home, provas, problemas, busca, buscaprob

app_name = 'provas_obi'
urlpatterns = [
    path('', provas, name='url_provas'),
    path('<int:pk>/problemas/', problemas, name='url_prob'),
    path('busca/', busca, name='url_busca'),
    path('buscaproblemas/', buscaprob, name='url_buscaprob'),
]