from django.shortcuts import render, redirect
from .models import Especialidades, DadosMedico, is_medico, DatasAbertas
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from datetime import datetime

def cadastro_medico(request):

    if request.method == "GET":
        especialidades = Especialidades.objects.all()
        return render(request, 'cadastro_medico.html', {'especialidades': especialidades})
    elif request.method == "POST":

        if is_medico(request.user):
            messages.add_message(request, constants.WARNING, 'Você já está cadastrado como médico.')
            return redirect('/medicos/abrir_horario')

        crm = request.POST.get('crm')
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        cim = request.FILES.get('cim')
        rg = request.FILES.get('rg')
        foto = request.FILES.get('foto')
        especialidade = request.POST.get('especialidade')
        descricao = request.POST.get('descricao')
        valor_consulta = request.POST.get('valor_consulta')

        dados_medico = DadosMedico(
            crm=crm,
            nome=nome,
            cep=cep,
            rua=rua,
            bairro=bairro,
            numero=numero,
            rg=rg,
            cedula_identidade_medica=cim,
            foto=foto,
            user=request.user,
            descricao=descricao,
            especialidade_id=especialidade,
            valor_consulta=valor_consulta
        )
        dados_medico.save()

        messages.add_message(request, constants.SUCCESS, 'Cadastro médico realizado com sucesso.')

        return redirect('/medicos/abrir_horario')
    
def abrir_horario(request):

    if (request.user == DadosMedico.objects.filter(user=request.user).exists()) == True:
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/pacientes/home')


    if request.method == "GET":
        dados_medicos = DadosMedico.objects.get(user=request.user)
        return render(request, 'abrir_horario.html', {'dados_medicos': dados_medicos})
    elif request.method == "POST":
        data = request.POST.get('data ')
        data_formatada = datetime.strptime(data, "%Y-%m-%dT%H:%M")

    if data_formatada <= datetime.now():
            messages.add_message(request, constants.WARNING, 'A data deve ser maior ou igual a data atual.')
            return redirect('/medicos/abrir_horario')
    
    horario_abrir = DatasAbertas(
        data=data,
        user=request.user
    )
    
    horario_abrir.save()
    
    messages.add_message(request, constants.SUCCESS, 'Horário cadastrado com sucesso.')
    return redirect('/medicos/abrir_horario')