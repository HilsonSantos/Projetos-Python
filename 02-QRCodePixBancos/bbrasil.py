from enum import global_str

import requests
from gerartoken import get_acess_token_bbrasil

url_cobranca_imediata = "https://api.hm.bb.com.br/pix/v2/cob"
url_cobranca_vencimento = "https://api.hm.bb.com.br/pix/v2/cobv"
url_simulacao_pagamento = "https://api.hm.bb.com.br/testes-portal-desenvolvedor/v1/boletos-pix/pagar"
url_consulta_pix_recebido = "https://api.hm.bb.com.br/pix/v2/pix"


class ApiPixCobrancaImediata(object):

    def __init__(self):
        self.token = get_acess_token_bbrasil()["access_token"]
        self.gwdevappkey = "1684b6826718dfbf3323dd4b5847ddd7"
        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        self.params = {"gw-dev-app-key": f"{self.gwdevappkey}"}
        self.url = None

    def cobranca_imediata_definidausuario(self):
        """ CRIA UMA COBRANÇA IMEDIATA, COM TXID DEFINIDO PELO USUÁRIO RECEBEDOR """
        self.url = url_cobranca_imediata
        txid = "CadanDistribuicao01Rem0000000002"
        payload = {
            "calendario": {
                "expiracao": 3600
            },
            "devedor": {
                "cnpj": "12345678901234",
                "nome": "Odorico Paraguacu"
            },
            "valor": {
                "original": "12.34"
            },
            "chave": "hmtestes2@bb.com.br",
            "solicitacaoPagador": "Serviço realizado.",
            "infoAdicionais": [
                    {"nome": "TESTE", "valor": "12.34"}
            ]
        }
        requisicao = requests.put(url=f"{self.url}/{txid}", data="", json=payload, headers=self.headers, params=self.params)
        resposta = requisicao.json()
        dicionario = dict(resposta)
        # print(dicionario["pixCopiaECola"])
        # gerarqrcode = GerarQrCodePix()
        # gerarqrcode.gerar_qr_code(dicionario["pixCopiaECola"])

        return print(dicionario)

    def cobranca_imediata_definidabanco(self):
        """ CRIA UMA COBRANÇA IMEDIATA, COM TXID DEFINIDO PELO BANCO """
        self.url = url_cobranca_imediata
        payload = {
            "calendario": {
                "expiracao": 3600
            },
            "devedor": {
                "cnpj": "12345678901234",
                "nome": "Odorico Paraguacu"
            },
            "valor": {
                "original": "13.00"
            },
            "chave": "9e881f18-cc66-4fc7-8f2c-a795dbb2bfc1",
            "solicitacaoPagador": "Serviço realizado.",
            "infoAdicionais": [
                    {"nome": "TESTE", "valor": "12.34"}
            ]
        }

        requisicao = requests.post(url=self.url, data="", json=payload, headers=self.headers, params=self.params)
        resposta = requisicao.json()
        dicionario = dict(resposta)
        # print(dicionario["pixCopiaECola"])
        # gerarqrcode = GerarQrCodePix()
        # gerarqrcode.gerar_qr_code(dicionario["pixCopiaECola"])

        return print(dicionario)

    def consultar_cobranca_imediata(self):
        """ CONSULTA UMA LISTA DE COBRANÇAS IMEDIATAS """
        self.url = url_cobranca_imediata
        params = {
            "gw-dev-app-key": "1684b6826718dfbf3323dd4b5847ddd7",
            "inicio": "2024-10-25T00:00:01Z",
            "fim": "2024-10-26T23:59:59Z",
            "cpf": "",
            "cnpj": "12345678901234",
            "locationPresente": "False",
            "status": "CANCELADA",
            "paginacao.paginaAtual": 0,
            "paginacao.itensPorPagina": 100
        }
        requisicao = requests.get(self.url, headers=self.headers, params=params)
        resposta = requisicao.json()
        lista = resposta["cobs"]
        for reg in lista:
            print(reg)

        return 1

    def simular_pagamento_pix(self):
        """ SIMULAÇÃO DE PAGAMENTO """
        self.url = url_simulacao_pagamento
        params = {
            "gw-app-key": "95cad3f03fd9013a9d15005056825665"
        }
        payload = {
            "pix": "00020101021226870014br.gov.bcb.pix2565qrcodepix-h.bb.com.br/pix/v2/326290b4-a392-4535-b91e-e70d586b82c9520400005303986540512.345802BR5921PAPELARIA LEITE CUNHA6012RONDONOPOLIS62070503***63044BDA"
        }
        requisicao = requests.post(url=self.url, json=payload, headers=self.headers, params=params)
        resposta = requisicao.json()

        return print(resposta)

    def consultar_lista_pixrecebidos(self):
        """ CONSULTAR UM LISTA DE PIX RECEBIDOS """
        self.url = url_consulta_pix_recebido
        params = {
            "gw-dev-app-key": "1684b6826718dfbf3323dd4b5847ddd7",
            "inicio": "2024-10-22T00:00:01Z",
            "fim": "2024-10-26T23:59:59Z",
            "cpf": "",
            "cnpj": "12345678000195",
            "paginacao.paginaAtual": 0,
            "paginacao.itensPorPagina": 100
        }

        requisicao = requests.get(url=self.url, data="payload", headers=self.headers, params=params)
        resposta = requisicao.json()
        dicionario = dict(resposta)

        return print(dicionario)

class ApiPixCobrancaVencimento(object):
    pass