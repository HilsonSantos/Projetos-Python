from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import *


def logoff():
    """ ESSA FUNÇÃO RETORNA A PÁGINA DE LOGIN """
    return redirect('/')


class Usuarios(object):
    def __init__(self):
        self.GET = None
        self.session = None

    def login(self):
        """ ESSA FUNÇÃO ELIMINA A ID DO USUÁRIO LOGADO NA SESSION """
        self.session.flush()
        return render(self, 'login.html', {'enviar': False})

    def autenticacao(self):
        """ ESSA FUNÇÃO VERIFICA SE O USUÁRIO PREENCHEU OS DADOS E VALIDA AS CREDENCIAIS """
        username = self.GET.get('username')
        password = self.GET.get('password')

        # SE O USUÁRIO E SENHA ESTIVER NÃO INFORMADOS, ENVIA UMA MENSAGEM.
        if len(username.strip()) == 0 and len(password.strip()) == 0:
            message = "Usuário e senha não informado."
            return render(self, 'login.html', {'enviar': True, 'message': message})
        # SE O USUÁRIO NÃO ESTIVER INFORMADO, ENVIA UMA MENSAGEM.
        elif len(username.strip()) == 0:
            message = "Usuário não informado."
            return render(self, 'login.html', {'enviar': True, 'message': message})
        # SE A SENHA NÃO ESTIVER INFORMADA, ENVIA UMA MENSAGEM.
        elif len(password.strip()) == 0:
            message = "Senha não informado."
            return render(self, 'login.html', {'enviar': True, 'message': message})
        else:
            try:
                # A VARIÁVEL RECEBER OS DADOS DO USUÁRIO LOGADO.
                user = User.objects.get(username=username)
                # A VARIÁVEL RECEBE A INFORMAÇÃO DO CAMPO ID.
                user_id = user.id
                # A VARIÁVEL RECEBE A INFORMAÇÃO DO CAMPO, SE ESTÁ ATIVO.
                isactive = user.is_active
                # SE O USUÁRIO ESTIVER INATIVO, ENVIA UMA MENSAGEM.
                if not isactive:
                    message = "Usuário está inativo."
                    return render(self, 'login.html', {'enviar': True, 'message': message})
                else:
                    # VERIFICA AS CREDENCIAIS DO USUÁRIO.
                    authentication = authenticate(username=username, password=password)
                    # SE AUTENTICIDADE FOR OK, ENTRA NO SISTEMA, CASO CONTRÁRIO, ENVIA UMA MENSAGEM.
                    if authentication is not None:
                        # GRAVA A INFORMAÇÃO DA ID DO USUÁRIO NO SESSION.
                        self.session['usuario_id'] = user_id
                        return redirect('/home/')
                    else:
                        message = "Senha inválida."
                        return render(self, 'login.html', {'enviar': True, 'message': message})
            except:
                message = "Usuário não cadastrado."
                return render(self, 'login.html', {'enviar': True, 'message': message})


def home(request):
    # VERIFICA SE A ID DO USUÁRIO ESTÁ NA SESSION, SE ESTIVER VAI PARA PÁGINA DO SISTEMA, CASO CONTRÁRIO
    # PERMANECE NA PÁGINA DE LOGIN E ENVIA UMA MENSAGEM.
    if request.session.get('usuario_id'):
        return render(request, 'home.html')
    else:
        message = "Precisa logar novamente no sistema."
        return render(request, 'login.html', {'enviar': True, 'message': message})


class CadastroClientes(object):
    def __init__(self):
        self.GET = None
        self.POST = None
        self.session = None

    def _list(self):
        clientes = Clientes.objects.all()
        dados = {
            'clientes': clientes
        }
        return render(self, 'clientes\clientes_listar.html', dados)

    def _insert(self):
        #
        cpf_cnpj = self.POST.get('cpf_cnpj')
        nrazaosocial = self.POST.get('nome_razaosocial')
        nfantasia = self.POST.get('nome_fantasia')
        tipo = self.POST.get('tipo')
        status = self.POST.get('status')
        #
        if tipo is None:
            tipo = 'J'
        #
        if status is None:
            status = 'A'

        consulta_cliente = Clientes.objects.filter(cpfcnpj=cpf_cnpj)

        if consulta_cliente.exists():
           pass
        else:
            #
            cliente = Clientes(
                cpfcnpj=cpf_cnpj,
                nrazaosocial=nrazaosocial,
                nfantasia=nfantasia,
                tipo=tipo,
                status=status
            )
            #
            cliente.save()

        return redirect('/clientes/')

    def update(self):
        pass

    def delete(self):
        pass
