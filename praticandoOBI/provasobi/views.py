from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Prova, Problema, Questao, Alternativa, ProvaPerson
from .forms import ProvaForm

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

    id_prob = []
    for p in problemas:
        id_prob.append(p)

    questoes = Questao.objects.all().select_related('codproblema').filter(codproblema__in=id_prob).order_by('numeroquestao')#.filter(codproblema__in=id_questoes)

    id_questoes = []
    for q in questoes:
         id_questoes.append(q)

    alternativas = Alternativa.objects.all().select_related('codquestao').filter(codquestao__in=id_questoes)

    return render(request, 'problemas.html', {'problemas': problemas, 'questoes': questoes, 'alternativas' : alternativas})
    #data = {}
    #data['problemas'] = Problema.objects.filter(pk=pk)
    #return render(request, 'problemas.html', data)

def provaperson(request):

    if request.method == "POST":
        form = ProvaForm(request.POST)
        if form.is_valid():
            provaperson = form.save(commit=False)
            provaperson.autor = request.user
            provaperson.save()
            return redirect('provaperson_detail', pk=provaperson.pk)
    else:
        form = ProvaForm()
    return render(request, 'provaperson.html', {'form':form})

def provaperson_detail(request, pk):
    provaperson = get_object_or_404(ProvaPerson, pk=pk)
    return render(request, 'provaperson_detail.html', {'provaperson':provaperson})