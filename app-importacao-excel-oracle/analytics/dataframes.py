
import pandas as pd
from sqlalchemy import text
from database.connection import get_oracle_engine
from config.config import ORACLE_SCHEMA

def consultar_industrias_foco():
    """

    :return:
    """
    engine = get_oracle_engine()
    sql = text(
        f"""
        SELECT
            COD_FORNECEDOR
            NOME_APRESENTACAO,
            FOCO
        FROM {ORACLE_SCHEMA}.CARGA_INDUSTRIASFOCO
        ORDER BY COD_FORNECEDOR
        """
    )
    with engine.connect() as connection:
        df = pd.read_sql(sql, connection)

    return df


def consultar_industrias_metas():
    """

    :return:
    """
    engine = get_oracle_engine()
    sql = text(
        f"""
        SELECT
            ID,
            DATA,
            COD_FORNECEDOR,
            COD_REPRESENTANTE,
            META_POSITIVACAO,
            META_FATURAMENTO
        FROM {ORACLE_SCHEMA}.CARGA_INDUSTRIASMETAS
        ORDER BY DATA
        """
    )
    with engine.connect() as connection:
        df = pd.read_sql(sql, connection)

    return df


def analisar_metas():
    """

    :return:
    """
    df = consultar_industrias_metas()
    resultado = (
        df.groupby("FORNECEDOR", dropna=False)
        ["META_FATURAMENTO"]
        .sum()
        .reset_index()
    )
    resultado = resultado.sort_values(
        "META_FATURAMENTO",
        ascending=False
    )
    return resultado
