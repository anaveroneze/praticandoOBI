from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from provasobi.models import ProvaPerson
from .forms import UserForm, ProfileForm, ProvaForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
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

def provaperson_info(request, pk):
    provaperson = get_object_or_404(ProvaPerson, pk=pk)
    return render(request, 'provapersoninfo.html', {'provaperson':provaperson})

def provaperson_lista(request):
    provaperson = get_object_or_404(ProvaPerson, pk=pk)
    return render(request, 'provapersoninfo.html', {'provaperson':provaperson})

def provaperson_nova(request):

    if request.method == "POST":
        form = ProvaForm(request.POST)
        if form.is_valid():
            provaperson = form.save(commit=False)
            provaperson.autor = request.user
            provaperson.save()
            return redirect('usuarios_obi:provaperson_info', pk=provaperson.pk)
    else:
        form = ProvaForm()
    return render(request, 'usuarios/provaperson.html', {'form':form})
