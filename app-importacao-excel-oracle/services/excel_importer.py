import logging
###############################################################################
from sqlalchemy import text
###############################################################################
from database.connection import get_oracle_engine
from config.config import ORACLE_SCHEMA, BATCH_SIZE
from services.data_transformer import preparar_para_oracle

# Configuração do logger
logger = logging.getLogger(__name__)

def importar_dataframe(connection, df, table: str):
    """

    :param connection:
    :param df:
    :param table:
    :return:
    """
    # Prepara os dados para Oracle
    df = preparar_para_oracle(df)

    # importa os resgistros em lotes
    df.to_sql(
        name=table,
        con=connection,
        schema=ORACLE_SCHEMA,
        if_exists="append",
        index=False,
        chunksize=BATCH_SIZE,
    )

    logger.info("%s registros enviados para %s", len(df), table)

def importar_planilha(df_foco, df_metas):
    """

    :param df_foco:
    :param df_metas:
    :return:
    """
    engine = get_oracle_engine()
    try:
        # Inicia uma única transação
        with engine.begin() as connection:
            logger.info("Iniciando importação para o Oracle")

            # Limpa a tabela de CARGA_INDUSTRIASFOCO
            connection.execute(text(f"DELETE FROM {ORACLE_SCHEMA}.CARGA_INDUSTRIASFOCO"))

            # Limpa a tabela de CARGA_INDUSTRIASMETAS
            connection.execute(text(f"DELETE FROM {ORACLE_SCHEMA}.CARGA_INDUSTRIASMETAS"))

            # Importar CARGA_INDUSTRIASFOCO
            df_foco = df_foco[
                [
                    "SEQFORNECEDOR",
                    "APRESENTACAO",
                    "FOCO"
                ]
            ]
            df_foco = df_foco.drop_duplicates(
                subset="SEQFORNECEDOR",
                keep="first"
            )
            importar_dataframe(connection, df_foco, "CARGA_INDUSTRIASFOCO")

            # Importar CARGA_INDUSTRIASMETAS
            df_metas = df_metas[
                [
                    "DATA",
                    "SEQFORNECEDOR",
                    "NROREPRESENTANTE",
                    "META_POSITIVACAO",
                    "META_FATURAMENTO"
                ]
            ]
            importar_dataframe(connection, df_metas, "CARGA_INDUSTRIASMETAS")

            logger.info("Importação concluída dentro da transação")

        logger.info("Transação confirmada com sucesso")

        return {
            "status": "SUCESSO",
            "industriasfoco": len(df_foco),
            "industriasmetas": len(df_metas),
            "total": len(df_foco) + len(df_metas)
        }
    except Exception as erro:
        logger.exception("Erro durante a importação: %s", erro)
        raise RuntimeError(
            "A importação foi cancelada. Verifique o log para identificar o erro."
        ) from erro