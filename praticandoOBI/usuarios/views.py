from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from provasobi.models import ProvaPerson, Prova, Questao, Classificacao, Problema, Alternativa
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import ProfileForm, ProvaForm, QuestoesForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.views.generic import (CreateView, DeleteView, DetailView, ListView)
from django.db.models import Q


#
# @login_required
def home_usuario(request):
    return render(request, 'usuarios/homeusuario.html', {})

def update_perfil(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil atualizado.')
            return redirect('home')
        else:
            messages.error(request, 'Corrija os erros.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'usuarios/perfil.html', {'user_form': user_form, 'profile_form': profile_form })

def cadastro_perfil(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.data_nascimento = form.cleaned_data.get('data_nascimento')
            user.profile.instituicao = form.cleaned_data.get('instituicao')
            user.profile.localizacao = form.cleaned_data.get('localizacao')
            user.save()
            messages.success(request, 'Perfil criado.')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('usuarios_obi:homeusuario')
    else:
        form = ProfileForm()
    return render(request, 'usuarios/signup.html', {'form': form})

def provaperson(request):

    if request.method == "POST":
        form = ProvaForm(request.POST)
        if form.is_valid():
            provaperson = form.save(commit=False)
            provaperson.autor = request.user.profile
            provaperson.save()
            # messages.success(request, 'Prova criada com sucesso! Adicione questões agora.')
            return redirect('usuarios_obi:questoes_busca', provaperson.pk)
            #return redirect('usuarios_obi:provaperson_detail', pk=provaperson.pk)
    else:
        form = ProvaForm()
    return render(request, 'novasprovas/provaperson.html', {'form':form})

def provaperson_edit(request, pk):
    provaperson = get_object_or_404(ProvaPerson, pk=pk)
    #apagar pois nao é POST
    if request.method == "POST":
        form = ProvaForm(request.POST, instance=provaperson)
        if form.is_valid():
            provaperson = form.save(commit=False)
            provaperson.autor = request.user.profile
            provaperson.save()
            return redirect('usuarios_obi:provaperson_detail', provaperson.pk)
    else:
        form = ProvaForm(instance=provaperson)
    return render(request, 'novasprovas/provaperson_edit.html', {'form':form, 'pk':pk})

#mostra as provas criadas
def provasperson(request):
    provas = ProvaPerson.objects.filter(autor=request.user.profile)
    return render(request, 'minhasprovas.html', {'provas': provas})


def provaperson_detail(request, pk):
    #provaperson = get_object_or_404(ProvaPerson, pk=pk)
    provaperson = ProvaPerson.objects.all().filter(pk=pk)
    return render(request, 'novasprovas/provaperson_detail.html', {'provaperson':provaperson})

def questoes_busca(request, pk):
    provaperson = get_object_or_404(ProvaPerson, pk=pk, autor=request.user.profile)
    error = False

    if 'q' in request.GET:
        q = request.GET['q']
        checkbox = request.GET.get("display_type", None)
        if not q:
            error = True
        else:
            if checkbox == 'provabox':
                provas = Prova.objects.filter(Q(anoprova=q) | Q(faseprova=q) | Q(nivelprova=q))
                return render(request, 'novasprovas/addquestoes_resultado.html', {'provaperson':provaperson, 'provas': provas, 'query': q, 'pk':pk})
            elif checkbox == 'problemabox':
                classificacao = Classificacao.objects.filter(tituloclassificacao=q)
                problemas = Problema.objects.filter(Q(tituloproblema__icontains=q) | Q(classificacao__in=classificacao))
                return render(request, 'novasprovas/addquestoes_resultado.html', {'provaperson': provaperson, 'problemas': problemas, 'query': q, 'pk': pk})
            elif checkbox == 'questaobox':
                return render(request, 'home.html', {})
            else:
                return render(request, 'home.html', {})
    return render(request, 'novasprovas/addquestoes.html', {'provaperson':provaperson,'error': error, 'pk': pk})


def questoes_add(request, codprova, pk):

    if request.method == "POST":
        provaperson = get_object_or_404(ProvaPerson, pk=codprova, autor=request.user.profile)
        id_questoes = request.POST.getlist('checks')
        for q in id_questoes:
            provaperson.questoes.add(q)
        return provaperson_pronta(request, codprova)

    else:
        problemas = Problema.objects.all().select_related('codprova').filter(codprova=pk)

        id_prob = []
        for p in problemas:
            id_prob.append(p)

        questoes = Questao.objects.all().select_related('codproblema').filter(codproblema__in=id_prob).order_by(
            'numeroquestao')  # .filter(codproblema__in=id_questoes)

        id_questoes = []
        for q in questoes:
            id_questoes.append(q)

        alternativas = Alternativa.objects.all().select_related('codquestao').filter(codquestao__in=id_questoes)

    return render(request, 'novasprovas/addquestoes_select.html',
                  {'problemas': problemas, 'questoes': questoes, 'alternativas': alternativas, 'pk':pk, 'codprova':codprova})

def provaperson_pronta(request, codprova):

    provaperson = get_object_or_404(ProvaPerson, pk=codprova, autor=request.user.profile)
    questoes = Questao.objects.all().filter(codquestao__in=provaperson.questoes.all()).order_by('numeroquestao')

    id_questoes = []
    for q in questoes:
        id_questoes.append(q)

    alternativas = Alternativa.objects.all().select_related('codquestao').filter(codquestao__in=id_questoes)

    id_problemas = Questao.objects.all().filter(codquestao__in=provaperson.questoes.all()).values('codproblema')
    problemas = Problema.objects.all().filter(codproblema__in=id_problemas).distinct()

    return render(request, 'novasprovas/provaperson_pronta.html', {'provaperson':provaperson, 'problemas':problemas, 'questoes': questoes, 'alternativas':alternativas, 'codprova':codprova})
