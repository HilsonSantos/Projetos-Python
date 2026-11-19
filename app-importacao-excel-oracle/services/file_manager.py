
import shutil
import logging
from pathlib import Path
from config.config import BASE_DIR, EXCEL_SOURCE

logger = logging.getLogger(__name__)


def copiar_planilha():
    """

    :return:
    """
    # Diretório de origem
    diretorio_origem = Path(EXCEL_SOURCE)

    # Nome do arquivo
    nome_arquivo = "DADOS_FORNECEDORES.xlsx"

    # Caminho completo de origem
    arquivo_origem = diretorio_origem / nome_arquivo

    # Diretório data da aplicação
    diretorio_destino = BASE_DIR / "data"

    # Cria o diretório caso não exista
    diretorio_destino.mkdir(
        parents=True,
        exist_ok=True
    )

    # Caminho completo de destino
    arquivo_destino = diretorio_destino / nome_arquivo

    # Verifica se o arquivo existe
    if not arquivo_origem.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {arquivo_origem}"
        )

    # Copia a planilha
    shutil.copy2(
        arquivo_origem,
        arquivo_destino
    )

    logger.info("Planilha copiada: %s", arquivo_destino)
    return arquivo_destino
