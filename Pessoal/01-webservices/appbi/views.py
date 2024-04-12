from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import pandas as pd


def painel01(request):
    """ Chama o dashboard no navegdor da web """
    template = 'painel01.html'
    return render(request=request, template_name=template)


def analise_dados(request):
    """ Pega dos dados nas planilhas e transforma em json para o javascript """
    # Caminho dos dados
    path = 'data'

    # Faz com que aparece todas as colunas do DataFrame
    pd.set_option('display.max_columns', None)

    # Formata os valores do DataFrame com 2 casas decimais
    pd.options.display.float_format = '{:.2f}'.format

    # DADOS DE LOJAS
    df_lojas = pd.read_excel(f'{path}/lojas.xlsx')
    df_lojas.columns = [
        'LojaId',
        'LojaNome',
        'LojaColaboradoresQtd',
        'LojaTipo',
        'LocalidadeId',
        'LojaGerente',
        'LojaGerenteDoc'
    ]
    df_lojas = df_lojas[['LojaId', 'LojaNome', 'LojaGerente', 'LojaTipo', 'LocalidadeId']].copy()

    # DADOS DE CLIENTES
    df_clientes = pd.read_excel(f'{path}/clientes.xlsx')
    df_clientes['ClienteNome'] = df_clientes['Primeiro Nome']+' '+df_clientes['Sobrenome']
    df_clientes = df_clientes.drop(columns=['Primeiro Nome', 'Sobrenome'])
    df_clientes.columns = [
        'ClienteId',
        'ClienteEmail',
        'ClienteSexo',
        'ClienteDtaNascimento',
        'ClienteEstadoCivel',
        'ClienteNumFilhos',
        'ClienteEscolaridade',
        'ClienteDocumento',
        'ClienteNome'
    ]
    df_clientes = df_clientes[['ClienteId', 'ClienteNome']].copy()

    # DADOS DE PRODUTOS
    df_produtos = pd.read_excel(f'{path}/Produtos.xlsx')
    df_produtos.columns = [
        'ProdutoSku',
        'ProdutoDescricao',
        'ProdutoMarca',
        'ProdutoTipo',
        'ProdutoPrecoUnitario',
        'ProdutoCustoUnitario',
        'ProdutoObservacao'
    ]

    # DADOS DE VENDAS
    df_vendas2022 = pd.read_excel(f'{path}/Vendas2022.xlsx')
    df_vendas2023 = pd.read_excel(f'{path}/Vendas2023.xlsx')
    df_vendas2024 = pd.read_excel(f'{path}/Vendas2024.xlsx')
    df_vendas = pd.concat(objs=[df_vendas2022, df_vendas2023, df_vendas2024], ignore_index=True).copy()
    df_vendas.columns = [
        'VendaData',
        'OrdemCompra',
        'ProdutoSku',
        'ClienteId',
        'VendaQuantidade',
        'LojaId'
    ]
    df_vendas = pd.merge(df_vendas, df_clientes, on='ClienteId', how='inner').copy()
    df_vendas = df_vendas.merge(df_lojas, left_on='LojaId', right_on='LojaId', how='inner').copy()
    df_vendas = df_vendas.merge(df_produtos, left_on='ProdutoSku', right_on='ProdutoSku', how='inner').copy()
    df_vendas['VendaTotal'] = df_vendas['VendaQuantidade'] * df_vendas['ProdutoPrecoUnitario']
    df_vendas['VendaAno'] = df_vendas['VendaData'].dt.year
    df_vendas['VendaMes'] = df_vendas['VendaData'].dt.month

    li_vendastotalvalorano = list()
    df_vendastotalvalorano = df_vendas.groupby(by='VendaAno', sort=True)['VendaTotal'].sum().reset_index()
    li_vendastotalvalorano.append(df_vendastotalvalorano.columns.tolist())
    for lista in df_vendastotalvalorano.values:
        li_vendastotalvalorano.append(lista.tolist())

    li_vendastotalvalormes = list()
    df_vendastotalvalormes = df_vendas[df_vendas['VendaAno'] == 2022].groupby(by='VendaMes', sort=True)['VendaTotal'].sum().reset_index()
    li_vendastotalvalormes.append(df_vendastotalvalormes.columns.tolist())
    for lista in df_vendastotalvalormes.values:
        li_vendastotalvalormes.append(lista.tolist())

    data = {
        'VendasTotalAno': li_vendastotalvalorano,
        'VendasTotalMes': li_vendastotalvalormes
    }

    return JsonResponse(data)