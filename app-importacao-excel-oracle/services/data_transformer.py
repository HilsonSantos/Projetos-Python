
import pandas as pd

def transformar_foco(df: pd.DataFrame) -> pd.DataFrame:
    # Cria uma cópia do DataFrame. Assim, preservamos os dados originais
    df = df.copy()
    # Padroniza os nomes das colunas
    df.columns = df.columns.str.strip()
    # Renomeia as colunas do Excel
    df = df.rename(
        columns={
            "COD_FORNECEDOR": "SEQFORNECEDOR",
            "COD_REPRESENTANTE": "NROREPRESENTANTE",
            "NOME_APRESENTACAO": "APRESENTACAO"
        }
    )
    df["SEQFORNECEDOR"] = pd.to_numeric(df["SEQFORNECEDOR"], errors="raise").astype("int64")
    df["NROREPRESENTANTE"] = pd.to_numeric(df["NROREPRESENTANTE"], errors="raise").astype("int64")
    df["APRESENTACAO"] = df["APRESENTACAO"].astype("string").str.strip()
    df["FOCO"] = df["FOCO"].astype("string").str.strip().str.upper()
    df = df[
        [
            "SEQFORNECEDOR",
            "NROREPRESENTANTE",
            "APRESENTACAO",
            "FOCO"
        ]
    ]
    return df


def transformar_metas(df: pd.DataFrame) -> pd.DataFrame:
    # Cria uma cópia do DataFrame. Assim, preservamos os dados originais
    df = df.copy()
    # Remove espaços dos nomes das colunas
    df.columns = df.columns.str.strip()
    # Renomeia as colunas do Excel
    df = df.rename(
        columns={
            "COD_FORNECEDOR": "SEQFORNECEDOR",
            "COD_REPRESENTANTE": "NROREPRESENTANTE",
            "META DE POSITIVAÇÃO": "META_POSITIVACAO",
            "META DE FATURAMENTO": "META_FATURAMENTO"
        }
    )
    df["DATA"] = pd.to_datetime(df["DATA"], errors="raise")
    df["SEQFORNECEDOR"] = pd.to_numeric(df["SEQFORNECEDOR"], errors="raise").astype("int64")
    df["NROREPRESENTANTE"] = pd.to_numeric(df["NROREPRESENTANTE"], errors="raise").astype("int64")
    df["META_POSITIVACAO"] = pd.to_numeric(df["META_POSITIVACAO"], errors="raise").astype("Int64")
    df["META_FATURAMENTO"] = pd.to_numeric(df["META_FATURAMENTO"], errors="raise")
    df["NOME_APRESENTACAO"] = df["NOME_APRESENTACAO"].astype("string").str.strip()
    df["FORNECEDOR"] = df["FORNECEDOR"].astype("string").str.strip()
    df = df[
        [
            "DATA",
            "SEQFORNECEDOR",
            "NROREPRESENTANTE",
            "META_POSITIVACAO",
            "META_FATURAMENTO"
        ]
    ]
    return df

def preparar_para_oracle(df: pd.DataFrame) -> pd.DataFrame:
    # Converte NaN, NaT e pd.NA em None para que sejam enviados como NULL ao Oracle
    return df.astype(object).where(pd.notna(df), None)
