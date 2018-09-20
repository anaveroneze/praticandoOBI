from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from provasobi.models import ProvaPerson
from .forms import UserForm, ProfileForm, ProvaForm, PerfilForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)
from django.views.decorators.csrf import csrf_protect

# Create your views here.
@csrf_protect
class entrar_perfil(CreateView):
    model = User
    form = PerfilForm
    template_name = 'usuarios/entrar_form.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

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

    user = User.objects.get(username=request.user)
    model = ProvaPerson
    ordering = ('codprovaperson', )
    template_name = 'usuarios/minhasprovas.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes\
            .select_related('titulo') \
            .annotate(questions_count=Count('questoes', distinct=True))
        return queryset

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
