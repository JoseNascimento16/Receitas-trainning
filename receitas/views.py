from django.core import paginator
from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Receita
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#from django.http import HttpResponse
        
def index(request):
    #dicionario receitas removido em aulas futuras
    receitas = Receita.objects.order_by('-date_receita').filter(publicada=True)
    paginator = Paginator(receitas, 3)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)
    dados = {
        #'receitas' : receitas
        'receitas' : receitas_por_pagina
    }

    return render(request, 'index.html', dados)

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    receita_a_exibir = {
        'receita' : receita
    }

    return render(request,'receita.html', receita_a_exibir)

def buscar(request):
    busca_receitas = Receita.objects.order_by('-date_receita').filter(publicada=True)

    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        if buscar:
            busca_receitas = busca_receitas.filter(nome_receita__icontains=nome_a_buscar)
            #Note que este "__icontains" tem a função de aceitar pedaços da palavra (não precisa digitar o nome da receita completamente)
    
    dados = {
        'receitas' : busca_receitas
    }

    return render(request, 'buscar.html', dados)