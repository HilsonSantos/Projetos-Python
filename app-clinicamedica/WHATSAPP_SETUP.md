# WhatsApp de teste

O envio é feito pela WhatsApp Business Cloud API. A Meta oferece números de teste gratuitos para desenvolvimento; o número que receberá mensagens deve estar autorizado na configuração de teste do app.

1. No painel Meta for Developers, configure o produto WhatsApp e obtenha o token de teste e o Phone Number ID.
2. Autorize o telefone destinatário no painel de teste.
3. Configure um modelo aprovado que aceite uma variável de texto no corpo para receber o link seguro.
4. Copie `.env.example` para `.env` e preencha o token, Phone Number ID, nome exato do modelo e idioma aprovado.
5. Recrie o serviço `app` para carregar as variáveis do `.env`.

Não envie o arquivo `.env` ao controle de versão. O serviço informa falha no formulário se as credenciais, o destinatário ou o modelo não estiverem prontos.
