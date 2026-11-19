#-- INICIALIZAR ORACLE E CRIAR ENGINE                                       --#
###############################################################################
import oracledb
""" Utilizada para conectar aplicação ao banco de dados oracle """
###############################################################################
from functools import lru_cache
""" 
O lru_cache é um recurso nativo do Python utilizado  para armazenar  em memória
de uma função, evitando que ela  precise executar novamente  quando receber  os
mesmos parâratros.
"""
###############################################################################
from sqlalchemy import create_engine
"""
Função do SQLAlchemy utilizada para criar uma conexão com o banco de dados.
"""
###############################################################################
from sqlalchemy.engine import URL
"""
URL: Permite construir URLs de conexão de maneira estruturada e segura.
"""
###############################################################################
from config.config import (
    ORACLE_HOST,
    ORACLE_PORT,
    ORACLE_SERVICE,
    ORACLE_SCHEMA,
    ORACLE_USER,
    ORACLE_PASSWORD,
    ORACLE_MODE,
    ORACLE_CLIENT,
    validar_configuracoes
)

""" Inicialização do Oracle Client no modo Thick """
if ORACLE_MODE == "thick":
    oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT)
else:
    oracledb.init_oracle_client()

def oracle_url() -> URL:
    """
    Construir a URL de conexão com o banco de dados Oracle utilizando as confi-
    gurações armazenadas nas variáveis de ambiente.
    :return: URL de conexão de maneira estruturada..
    """
    validar_configuracoes()
    return URL.create(
        drivername="oracle+oracledb",
        username=ORACLE_USER,
        password=ORACLE_PASSWORD,
        host=ORACLE_HOST,
        port=ORACLE_PORT,
        query={"service_name": ORACLE_SERVICE}
    )

@lru_cache(maxsize=1)
# Esse decoracor faz com que o resultado da função fique armazenado em memória.
# O maxsize=1, significa que será armazenado apenas um resultado.
def get_oracle_engine() -> Engine:
    """
    Cria o mecanismo de conexão com Oracle e reutilizá-lo durante a execução da
    aplicação.
    :return:
    """
    engine = create_engine(
        oracle_url(),
        pool_pre_ping=True, # Verifica se a conexão do pool está ativa antes de reutilizá-la.
        hide_parameters=True,
        pool_size=5, # Mantém até 5 conexões permanentes no pool.
        max_overflow=10, # Permite até 10 conexões adicionais temporárias.
        pool_recycle=1800, # Recicla conexões após 1800 segundos de utilização.
    )
    return engine

def testar_conexao():
    """

    :return:
    """
    engine = get_oracle_engine()
    with engine.connect() as connection:
        resultado = connection.exec_driver_sql("SELECT SYSDATE FROM DUAL")
        data_oracle = resultado.scalar_one()
        print("Conexão Oracle realizada com sucesso!")
        print(f"Data do Oracle: {data_oracle}")


def fechar_conexao():
    """
    Encerrar o gerenciamento das conexões e limpar o cache do Engine.
    :return:
    """
    if get_oracle_engine.cache_info().currsize:
        get_oracle_engine().dispose()
        get_oracle_engine.cache_clear()
