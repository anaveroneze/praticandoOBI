from django.urls import path
from provasobi.views import home, provas, problemas

app_name = 'provas_obi'
urlpatterns = [
    path('', provas, name='url_provas'),
    path('<int:pk>/problemas/', problemas, name='url_prob'),
]