from django.contrib import admin
from .models import Prova, Classificacao, ProvaPerson

# # Register your models here.
admin.site.register(Prova)
admin.site.register(Classificacao)
admin.site.register(ProvaPerson)