#-- CARREGAR E VALIDAR CONFIGURAÇÕES                                        --#
###############################################################################
import os
"""
Disponibiliza funções para interagir com o sistema operacional,  incluindo lei-
tura de variáveis de ambiente.
"""
###############################################################################
from pathlib import Path
""" 
Permite trabalhar com caminhos  de arquivos independentemente  de barras do
Windows.
"""
###############################################################################
from dotenv import load_dotenv
""" Importa a função que carrega variáveis de uma arquivo .env. """
###############################################################################

""" Diretório principal do projeto """
BASE_DIR = Path(__file__).resolve().parent.parent

""" Carrega as variáveis do arquivo .env """
load_dotenv(BASE_DIR / ".env")

""" Configurações Oracle"""
ORACLE_HOST = os.getenv("ORACLE_HOST")
ORACLE_PORT = int(os.getenv("ORACLE_PORT"))
ORACLE_SERVICE = os.getenv("ORACLE_SERVICE")
ORACLE_SCHEMA = os.getenv("ORACLE_SCHEMA")
ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_MODE = os.getenv("ORACLE_MODE")
ORACLE_CLIENT = os.getenv("ORACLE_CLIENT")

""" Configurações Excel """
EXCEL_SOURCE = BASE_DIR / os.getenv("EXCEL_SOURCE")
EXCEL_FILE = BASE_DIR / os.getenv("EXCEL_FILE")

""" Quantidade de registros por lote """
BATCH_SIZE = int(os.getenv("BATCH_SIZE"))

""" Diretórios """
LOG_DIR = BASE_DIR / "logs"
EXPORT_DIR = BASE_DIR / "exports"

""" Cria diretórios caso não existam """
LOG_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)

def validar_configuracoes():
    """
    Verifica se as configurações essenciais foram preenchidas.
    :return:
    """
    # Paramêtros da conexão do Oracle que são obrigatórios
    parametros = {
        "ORACLE_HOST": ORACLE_HOST,
        "ORACLE_PORT": ORACLE_PORT,
        "ORACLE_SERVICE": ORACLE_SERVICE,
        "ORACLE_SCHEMA": ORACLE_SCHEMA,
        "ORACLE_USER": ORACLE_USER,
        "ORACLE_PASSWORD": ORACLE_PASSWORD,
    }

    ausentes = [
        nome
        for nome, valor in parametros.items()
        if not valor
    ]

    if ausentes:
        raise ValueError("Configurações ausentes: " + ", ".join(ausentes))

    if ORACLE_MODE not in ("thin", "thick"):
        raise ValueError("ORACLE_MODE deve ser thin ou thick")