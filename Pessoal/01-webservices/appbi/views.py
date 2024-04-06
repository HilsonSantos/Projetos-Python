from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import pandas as pd


def painel01(request):
    template = 'painel01.html'
    return render(request=request, template_name=template)


def analise_dados(request):
    path = 'data'
    # LOJAS
    df_lojas = pd.read_excel(f'{path}/lojas.xlsx')
    df_lojas.columns = [
        'LojaId',
        'LojaNome',
        'ColaboradoresQtd',
        'LojaTipo',
        'LocalidadeId',
        'LojaGerente',
        'GerenteDoc'
    ]
    df_lojas = df_lojas[['LojaId', 'LojaNome', 'LojaGerente', 'LojaTipo', 'LocalidadeId']]

    # CLIENTES
    df_clientes = pd.read_excel(f'{path}/clientes.xlsx')
    df_clientes['ClienteNome'] = df_clientes['Primeiro Nome']+' '+df_clientes['Sobrenome']
    df_clientes = df_clientes.drop(columns=['Primeiro Nome', 'Sobrenome'])
    df_clientes.columns = [
        'ClienteId',
        'Email',
        'Sexo',
        'DtaNascimento',
        'EstadoCivel',
        'NumFilhos',
        'Escolaridade',
        'Documento',
        'ClienteNome'
    ]
    df_clientes = df_clientes[['ClienteId', 'ClienteNome']]

    # VENDAS
    df_vendas2022 = pd.read_excel(f'{path}/Vendas2022.xlsx')
    df_vendas2023 = pd.read_excel(f'{path}/Vendas2023.xlsx')
    df_vendas2024 = pd.read_excel(f'{path}/Vendas2024.xlsx')
    df_vendas = pd.concat([df_vendas2022, df_vendas2023, df_vendas2024], ignore_index=True)
    df_vendas.columns = [
        'Data',
        'OrdemCompra',
        'Sku',
        'ClienteId',
        'QuantidadeVda',
        'LojaId'
    ]
    print(df_vendas)


    return HttpResponse('OK')