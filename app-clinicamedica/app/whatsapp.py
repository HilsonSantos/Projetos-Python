import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class WhatsAppNaoConfigurado(Exception):
    pass


class FalhaEnvioWhatsApp(Exception):
    pass


def enviar_link_redefinicao(telefone, link):
    token = os.environ.get("WHATSAPP_ACCESS_TOKEN")
    phone_number_id = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")
    template_name = os.environ.get("WHATSAPP_TEMPLATE_NAME")
    if not all((token, phone_number_id, template_name)):
        raise WhatsAppNaoConfigurado

    api_version = os.environ.get("WHATSAPP_API_VERSION", "v26.0")
    language = os.environ.get("WHATSAPP_TEMPLATE_LANGUAGE", "pt_BR")
    endpoint = f"https://graph.facebook.com/{api_version}/{phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": telefone,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language},
            "components": [{
                "type": "body",
                "parameters": [{"type": "text", "text": link}],
            }],
        },
    }
    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=15) as response:
            if response.status < 200 or response.status >= 300:
                raise FalhaEnvioWhatsApp
    except (HTTPError, URLError, TimeoutError) as exc:
        raise FalhaEnvioWhatsApp from exc
