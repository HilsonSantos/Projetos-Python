import pandas as pd
from pathlib import Path
from config.config import EXCEL_FILE

def ler_planilha(path: str | Path = EXCEL_FILE, sheet: str = None) -> pd.DataFrame:
    """
    A função lê a planilha Excel e retorna um DataFrame.
    :param path: Caminho do arquivo Excel.
    :param sheet: Nome da aba.
    :return: DataFrame com os dados.
    """
    try:
        # Verifica se o arquivo existe
        arquivo = Path(path)
        if not arquivo.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")

        # Lê a aba do Excel
        df = pd.read_excel(path, sheet_name=sheet, engine="openpyxl")

        # Remove espaços dos nomes das colunas
        df.columns = df.columns.str.strip()

        # Remove linhas completamente vazias
        df = df.dropna(how="all")

        # Reinicia o índice
        df = df.reset_index(drop=True)

        return df
    except Exception as erro:
        raise RuntimeError(
            f"Erro ao ler a aba '{sheet}' do arquivo '{path}': {erro}"
        ) from erro


def ler_abas_planilha(path: str | Path = EXCEL_FILE) -> dict[str, pd.DataFrame]:
    """
    A função lê todas as abas em um único comando
    :param path: Caminho do arquivo Excel.
    :return: Dicionario com os dados de um DataFrames.
    """
    planilhas = pd.read_excel(path, sheet_name=None, engine="openpyxl")
    resultado = {}
    for sheet, df in planilhas.items():
        df.columns = df.columns.astye(str).str.strip()
        df = df.dropna(how="all")
        df = df.reset_index(drop=True)
        resultado[sheet] = df

    return resultado