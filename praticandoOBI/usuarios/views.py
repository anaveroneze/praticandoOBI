from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from provasobi.models import ProvaPerson
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import ProfileForm, ProvaForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.views.generic import (CreateView, DeleteView, DetailView, ListView)
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
            messages.success(request, 'Prova criada.')
            return redirect('home')
            #return redirect('usuarios_obi:provaperson_detail', pk=provaperson.pk)
    else:
        form = ProvaForm()
    return render(request, 'novasprovas/provaperson.html', {'form':form})

#mostra as provas criadas
def provasperson(request):
    provas = ProvaPerson.objects.filter(autor=request.user.profile)
    return render(request, 'minhasprovas.html', {'provas': provas})


def provaperson_detail(request, pk):
    #provaperson = get_object_or_404(ProvaPerson, pk=pk)
    provaperson = ProvaPerson.objects.all().filter(pk=pk)
    return render(request, 'novasprovas/provaperson_detail.html', {'provaperson':provaperson})