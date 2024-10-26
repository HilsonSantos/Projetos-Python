import requests
from gerartoken import get_acess_token_bsantander


def processo_bancosantander(opcao):
    token = get_acess_token_bsantander()['access_token']
    url = "https://pix.santander.com.br"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    # CRIA COBRANÇA IMEDIATA #
    if opcao == 1:
        txid = "RCADAN700899740001790000000001"
        payload = {
            "calendario": {"expiracao": 3600},
            "devedor": {"cnpj": "12345678000195", "nome": "Teste"},
            "valor": {"original": "200.00"},
            "chave": "7d9f0335-8dcc-4054-9bf9-0dbd61d36906",
            "solicitacaoPagador": "Serviço realizado.",
            "infoAdicionais": [
                    {"nome": "HILSON", "valor": "70.00"},
                    {"nome": "SALMO", "valor": "80.00"},
                    {"nome": "EDILSON", "valor": "50.00"}
            ]
        }
        requisicao = requests.put(url=f"{url}/pix/cob/{txid}", json=payload, headers=headers)
        print(requisicao.status_code)
        #resposta = requisicao.json()
        #dicionario = dict(resposta)
        #print(dicionario)
        #gerarqrcode = GerarQrCodePix()
        #gerarqrcode.gerar_qr_code(dicionario["pixCopiaECola"])
    elif opcao == 2:
        pass