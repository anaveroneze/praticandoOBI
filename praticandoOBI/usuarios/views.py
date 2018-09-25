from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from provasobi.models import ProvaPerson, Prova, Questao
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
            messages.success(request, 'Prova criada com sucesso! Adicione questões agora.')
            return redirect('usuarios_obi:provaperson_edit', provaperson.pk)
            #return redirect('usuarios_obi:provaperson_detail', pk=provaperson.pk)
    else:
        form = ProvaForm()
    return render(request, 'novasprovas/provaperson.html', {'form':form})

def provaperson_edit(request, pk):
    provaperson = get_object_or_404(ProvaPerson, pk=pk)
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

def questoes_add(request, pk):
    provaperson = get_object_or_404(ProvaPerson, pk=pk, autor=request.user.profile)
    error = False

    if 'q' in request.GET:
        q = request.GET['q']
        checkbox = request.GET.get("display_type", None)
        if not q:
            error = True
        else:
            if  checkbox == 'provabox':
                provas = Prova.objects.filter(Q(anoprova=q) | Q(faseprova=q) | Q(nivelprova=q))
                return render(request, 'novasprovas/addquestoes_resultado.html', {'provaperson':provaperson, 'provas': provas, 'query': q})
            elif checkbox == 'problemabox':
                classificacao = Classificacao.objects.filter(tituloclassificacao=q)
                provas = Problema.objects.filter(
                    Q(tituloproblema__icontains=q) | Q(classificacao__in=classificacao))
                return render(request, 'novasprovas/addquestoes_resultado.html',
                              {'provaperson': provaperson, 'provas': provas, 'query': q})
            elif checkbox == 'questaobox':
                return render(request, 'home', {})
            else:
                return render(request, 'home', {})

    return render(request, 'novasprovas/addquestoes.html', {'provaperson':provaperson,'error': error})



# def question_add(request, pk):
#
#     quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)
#     if request.method == 'POST':
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             question = form.save(commit=False)
#             question.quiz = quiz
#             question.save()
#             messages.success(request, 'You may now add answers/options to the question.')
#             return redirect('teachers:question_change', quiz.pk, question.pk)
#     else:
#         form = QuestionForm()
#
#     return render(request, 'classroom/teachers/question_add_form.html', {'quiz': quiz, 'form': form})