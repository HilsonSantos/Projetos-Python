from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


def login(request):
    """ Essa função elimina a id do usuário logado """
    request.session.flush()
    return render(request, 'login.html', {'tipo': False})


def logoff(request):
    """ Essa função retorna a página de login """
    return redirect('/')


def autenticacao(request):
    """ Essa função verifica se o usuário preencheu os dados e valida as credenciais do mesmo """

    username = request.GET.get('usuario')
    password = request.GET.get('senha')

    # Se o usuário e senha estiver sem informação, envia uma mensagem.
    if len(username.strip()) == 0 and len(password.strip()) == 0:
        message = "Usuário e senha não informado."
        return render(request, 'login.html', {'tipo': True, 'message': message})
    # Se o usuário não estiver informado, envia uma mensagem.
    elif len(username.strip()) == 0:
        message = "Usuário não informado."
        return render(request, 'login.html', {'tipo': True, 'message': message})
    # Se a senha não estiver informado, envia uma mensagem.
    elif len(password.strip()) == 0:
        message = "Senha não informado."
        return render(request, 'login.html', {'tipo': True, 'message': message})
    else:
        try:
            # Recebe os dados do usuário logado.
            user = User.objects.get(username=username)
            # Recebe a informação do campo se está ativo.
            isactive = user.is_active
            # Se o usuário estiver inativo, envia uma mensagem.
            if not isactive:
                message = "Usuário está inativo."
                return render(request, 'login.html', {'tipo': True, 'message': message})
            else:
                # Verifica as credenciais do usuário.
                authentication = authenticate(username=username, password=password)
                # Se autenticidade for OK, entra no sistema, caso contrário, envia uma mensagem.
                if authentication is not None:
                    user = User.objects.get(username=username)
                    request.session['usuario_id'] = user.id
                    return redirect('/home/')
                else:
                    message = "Senha inválida."
                    return render(request, 'login.html', {'tipo': True, 'message': message})
        except:
            message = "Usuário não cadastrado."
            return render(request, 'login.html', {'tipo': True, 'message': message})


def home(request):
    if request.session.get('usuario_id'):
        return render(request, 'home.html')
    else:
        message = "Precisa logar novamente no sistema."
        return render(request, 'login.html', {'tipo': True, 'message': message})


def tabelas_lista(request):
    return render(request, 'criar_tabelas.html')


def selects_lista(request):
    return render(request, 'criar_selects.html')


def configuracoes(request):
    return render(request, 'configuracoes.html')
