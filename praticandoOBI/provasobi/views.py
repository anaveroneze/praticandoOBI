from django.shortcuts import render, redirect
from .models import Prova, Problema
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
    #for p in problemas:
    #    print(p.tituloproblema)
    return render(request, 'problemas.html', {'problemas': problemas})
    #data = {}
    #data['problemas'] = Problema.objects.filter(pk=pk)
    #return render(request, 'problemas.html', data)


