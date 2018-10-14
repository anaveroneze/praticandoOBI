# -*- coding: utf-8 -*-
import codecs
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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.conf.urls.static import static
from django.conf import settings
from django.core.files import File

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
            return redirect('home')
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
            messages.success(request, "Alterações salvas!")
            return redirect('usuarios_obi:provaperson_edit', provaperson.pk)
    else:
        form = ProvaForm(instance=provaperson)
    return render(request, 'novasprovas/provaperson_edit.html', {'form':form, 'pk':pk, 'titulo':provaperson.titulo, 'ano':provaperson.ano, 'dificuldade':provaperson.dificuldade, 'obs':provaperson.observacoes})

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
            if q.isnumeric() == False:
                return redirect('usuarios_obi:questoes_busca', provaperson.pk)
            elif checkbox == 'anoox':
                provas = Prova.objects.filter(Q(anoprova=q))
                return render(request, 'novasprovas/addquestoes_resultado.html', {'provaperson':provaperson, 'provas': provas, 'query': q, 'pk':pk})
            elif checkbox == 'fasebox':
                provas = Prova.objects.filter(Q(faseprova=q))
                return render(request, 'novasprovas/addquestoes_resultado.html', {'provaperson': provaperson, 'provas': provas, 'query': q, 'pk': pk})

                # classificacao = Classificacao.objects.filter(tituloclassificacao=q)
                # problemas = Problema.objects.filter(Q(tituloproblema__icontains=q) | Q(classificacao__in=classificacao))
                # return render(request, 'novasprovas/addquestoes_resultado.html', {'provaperson': provaperson, 'problemas': problemas, 'query': q, 'pk': pk})
            elif checkbox == 'nivelbox':
                provas = Prova.objects.filter(Q(nivelprova=q))
                return render(request, 'novasprovas/addquestoes_resultado.html', {'provaperson': provaperson, 'provas': provas, 'query': q, 'pk': pk})
            else:
                provas = Prova.objects.filter(Q(anoprova=q) | Q(faseprova=q) | Q(nivelprova=q))
                return render(request, 'novasprovas/addquestoes_resultado.html', {'provaperson': provaperson, 'provas': provas, 'query': q, 'pk': pk})

        provas = Prova.objects.all()
        return render(request, 'novasprovas/addquestoes_resultado.html', {'provaperson': provaperson, 'provas': provas, 'query': q, 'pk': pk})

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

        init = []
        end = []
        count = 0

        for p in problemas:
            init.append(questoes[count].numeroquestao)
            for q in questoes:
                if q.codproblema.codproblema == p.codproblema:
                    count = count + 1
            end.append(questoes[count-1].numeroquestao)

        alternativas = Alternativa.objects.all().select_related('codquestao').filter(codquestao__in=id_questoes)

    return render(request, 'novasprovas/addquestoes_select.html',
                  {'problemas': problemas, 'questoes': questoes, 'alternativas': alternativas, 'pk':pk, 'codprova':codprova, 'init':init, 'end':end})

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


def provaperson_baixar(request, codprova):

    #ENCONTRA CONTEUDO DA PROVA:
    provaperson = get_object_or_404(ProvaPerson, pk=codprova, autor=request.user.profile)
    questoes = Questao.objects.all().filter(codquestao__in=provaperson.questoes.all()).order_by('numeroquestao')

    id_questoes = []
    for q in questoes:
        # print(q.enunciadoquestao) #ARRUMAR ACENTUAÇÃO
        id_questoes.append(q)

    alternativas = Alternativa.objects.all().select_related('codquestao').filter(codquestao__in=id_questoes)

    id_problemas = Questao.objects.all().filter(codquestao__in=provaperson.questoes.all()).values('codproblema')
    problemas = Problema.objects.all().filter(codproblema__in=id_problemas).distinct()

    #  ESCREVE NA PROVA
    count = 1

    doc = SimpleDocTemplate("/tmp/prova-" + str(codprova) + ".pdf", rightMargin=50, leftMargin=50, topMargin=40, bottomMargin=50)
    styles = getSampleStyleSheet()
    Story = [Spacer(1, 0.2 * inch)]
    style = styles["Normal"]

    par = Paragraph('<para align=center fontSize=20 > <b>' + provaperson.titulo + '</b></para>', style)
    Story.append(par)
    Story.append(Spacer(1, 0.4 * inch))

    for p in problemas:
        par = Paragraph('<para align=center fontSize=14><b>' + p.tituloproblema + '</b><br/></para>', style)
        Story.append(par)
        Story.append(Spacer(1, 0.2 * inch))
        par = Paragraph('<para fontSize=12>' + p.enunciadoproblema + '<br/></para>',style)
        Story.append(par)
        if p.regrasproblema:
            Story.append(Spacer(1, 0.1 * inch))
            par = Paragraph('<para fontSize=12><b>REGRAS:</b><br/></para>', style)
            Story.append(par)
            par = Paragraph('<para fontSize=12>' + p.regrasproblema + '<br/></para>', style)
            Story.append(par)
            Story.append(Spacer(1, 0.2 * inch))
        else:
            Story.append(Spacer(1, 0.2 * inch))
        if p.imgproblema:
            #local: 'static/ + p.imgproblema'
            #heroku: '/app/praticandoOBI/static/'
            img = Image( 'static/' + p.imgproblema, 4 * inch, 4*inch)
            Story.append(img)

        for q in questoes:
            if p.codproblema == q.codproblema.codproblema:
                par = Paragraph('<para fontSize=12><b>Questão ' + str(count) + "</b> - " + q.enunciadoquestao + '<br/></para>', style)
                Story.append(par)
                Story.append(Spacer(1, 0.2 * inch))
                count+=1
                if q.imgquestao:
                    # local: 'static/ + q.imgproblema'
                    img = Image('/app/praticandoOBI/static/' + q.imgproblema, 2 * inch, 2 * inch)
                    Story.append(img)
                for a in alternativas:
                    if a.codquestao.codquestao == q.codquestao:
                        par = Paragraph('<para fontSize=12><b>' + a.letraalternativa + ')</b> ' + a.textoalternativa + '<br/></para>', style)
                        Story.append(par)
                        Story.append(Spacer(1, 0.1 * inch))
        Story.append(Spacer(1, 0.3 * inch))
    doc.build(Story)
    nome = "prova-" + str(codprova)
    fs = FileSystemStorage("/tmp")
    with fs.open("prova-"+str(codprova)+".pdf") as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename='+nome+'.pdf'
    return response

def dadosbanco(request):
    download = get_object_or_404(ProvaPerson, autor=request.user.profile)

    path_to_file = '/app/praticandoOBI/OBI.db'
    f = open(path_to_file, 'r')
    myfile = File(f)
    response = HttpResponse(myFile, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="Banco"'
    # response = HttpResponse(myfile, content_type='application/vnd.ms-excel')
    # response['Content-Disposition'] = 'attachment; filename=' + name
    return response

    # response['Content-Disposition'] = 'attachment; filename="/app/praticandoOBI/OBI.db'
    # return response
    #fazer download do banco do heroku
   # os.sys(/app/praticandoOBI/OBI.db)