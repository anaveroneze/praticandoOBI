from django.shortcuts import render, redirect
from .models import Prova, Problema, Questao
from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
    data = {}
    data['provas'] = Prova.objects.all()
    return render(request, 'home.html', data)

def provas(request):
    data = {}
    data['provas'] = Prova.objects.all()
    return render(request, 'provas.html', data)

def problemas(request, pk):
    problemas = Problema.objects.all().select_related('codprova').filter(codprova=pk)
    questoes = Questao.objects.all().select_related('codprova').filter(codprova=pk)#.filter(codproblema__in=id_questoes)

    for q in questoes:
         print(q)
    for p in problemas:
         print(p)

    # for p in problemas:
    #     prob = p.codproblema
    #     id_questoes.append(prob)
    #     print(prob)
    return render(request, 'problemas.html', {'problemas': problemas, 'questoes': questoes})
    #data = {}
    #data['problemas'] = Problema.objects.filter(pk=pk)
    #return render(request, 'problemas.html', data)


