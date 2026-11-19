#-- INICIALIZAR E EXECUTAR A APLICAÇÃO                                      --#
###############################################################################
import logging
###############################################################################
import time
###############################################################################
from config.config import validar_configuracoes
from config.logging_config import  configurar_logs
from database.connection import testar_conexao, fechar_conexao
from services.excel_reader import ler_planilha
from services.data_validator import validar_industriasfoco, validar_industriasmetas
from services.data_transformer import transformar_foco, transformar_metas
from services.excel_importer import importar_planilha
from services.file_manager import copiar_planilha

configurar_logs()

logger = logging.getLogger(__name__)

def executar_importacao():
    inicio = time.perf_counter()
    try:
        logger.info("====================================")
        logger.info("INICIANDO PROCESSAMENTO EXCEL ORACLE")
        logger.info("====================================")

        # 1. Validar configurações
        validar_configuracoes()

        # 2. Testar conexão Oracle
        testar_conexao()

        # 3. Copia a planilha para a aplicação
        planilha = copiar_planilha()

        # 4. Ler aba INDUSTRIAS-FOCO
        df_foco = ler_planilha(planilha, "INDUSTRIAS-FOCO")
        logger.info("PLANILHA ABA INDUSTRIAS-FOCO: %s registros lidos", len(df_foco))

        # 5. Ler aba INDUSTRIAS-METAS
        df_metas = ler_planilha(planilha, "INDUSTRIAS-METAS")
        logger.info("PLANILHA ABA INDUSTRIAS-METAS: %s registros lidos", len(df_metas))

        # 6. Transformar os dados
        df_foco = transformar_foco(df_foco)
        df_metas = transformar_metas(df_metas)

        # 7. Validar os dados originais
        validar_industriasfoco(df_foco)
        validar_industriasmetas(df_metas)

        # 8. Importar para Oracle
        resultado = importar_planilha(df_foco, df_metas)

        # 9. Calcular duração
        duracao = (time.perf_counter() - inicio)
        logger.info("IMPORTAÇÃO FINALIZADA")
        logger.info("TABELA CARGA_INDUSTRIASFOCO: %s", resultado["industriasfoco"])
        logger.info("TABELA CARGA_INDUSTRIASMETAS: %s", resultado["industriasmetas"])
        logger.info("TOTAL DE REGISTROS: %s", resultado["total"])
        logger.info("DURAÇÃO: %.2f segundos", duracao)
        logger.info("STATUS: %s", resultado["status"])
    except Exception:
        logger.exception("FALHA NO PROCESSAMENTO")
        raise
    finally:
        fechar_conexao()

if __name__ == "__main__":
    executar_importacao()
