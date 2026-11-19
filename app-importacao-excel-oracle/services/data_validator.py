
import pandas as pd

# Colunas obrigatórias da aba FOCO
INDUSTRIAS_FOCO = [
    "SEQFORNECEDOR",
    "NROREPRESENTANTE",
    "APRESENTACAO",
    "FOCO"
]

# Colunas obrigatórias da aba METAS
INDUSTRIAS_METAS = [
    "DATA",
    "SEQFORNECEDOR",
    "NROREPRESENTANTE",
    "META_POSITIVACAO",
    "META_FATURAMENTO"
]

def validar_colunas(df: pd.DataFrame, colunas_obrigatorias: list):
    ausentes = [
        coluna
        for coluna in colunas_obrigatorias
        if coluna not in df.columns
    ]

    if ausentes:
        raise ValueError(f"Colunas ausentes: {ausentes}")


def validar_dataframe(df: pd.DataFrame, sheet: str):
    if df.empty:
        raise ValueError(f"A planilha {sheet} está vazia.")

    if df.isna().all(axis=1).any():
        raise ValueError(f"A planilha {sheet} possui linhas vazias.")

def validar_industriasfoco(df: pd.DataFrame):
    validar_colunas(df, INDUSTRIAS_FOCO)
    validar_dataframe(df, sheet="INDUSTRIAS-FOCO")
    campos_obrigatorios = [
        "SEQFORNECEDOR",
        "NROREPRESENTANTE",
        "APRESENTACAO",
        "FOCO"
    ]

    if df[campos_obrigatorios].isna().any().any():
        raise ValueError("Existem valores nulos nos campos obrigatórios de FOCO.")

    valores_foco = (
        df["FOCO"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    invalidos = ~valores_foco.isin(["SIM", "NÃO"])

    if invalidos.any():
        raise ValueError("FOCO deve conter somente SIM ou NÃO.")

    duplicados = df.duplicated(
        subset=["SEQFORNECEDOR", "NROREPRESENTANTE"],
        keep=False
    )

    if duplicados.any():
        raise ValueError("Existem duplicidades na chave de FOCO.")

def validar_industriasmetas(df: pd.DataFrame):
    validar_colunas(df, INDUSTRIAS_METAS)
    validar_dataframe(df, sheet="INDUSTRIAS-METAS")
    campos_obrigatorios = [
        "DATA",
        "SEQFORNECEDOR",
        "NROREPRESENTANTE",
        "META_POSITIVACAO",
        "META_FATURAMENTO"
    ]

    if df[campos_obrigatorios].isna().any().any():
        raise ValueError("Existem valores nulos nos campos obrigatórios de METAS.")
