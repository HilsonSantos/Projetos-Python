@echo off
setlocal

rem Run from this file's directory, regardless of the caller's working directory.
cd /d "%~dp0"
if errorlevel 1 (
    echo [ERRO] Nao foi possivel acessar a pasta da aplicacao.
    pause
    exit /b 1
)

set "VENV_PYTHON=%~dp0.venv\Scripts\python.exe"

rem Create the virtual environment and install dependencies on first run.
if not exist "%VENV_PYTHON%" (
    echo [INFO] Ambiente virtual nao encontrado. Criando...
    where py >nul 2>nul
    if not errorlevel 1 (
        py -3 -m venv ".venv"
    ) else (
        where python >nul 2>nul
        if errorlevel 1 (
            echo [ERRO] Python 3 nao foi encontrado. Instale Python 3 e tente novamente.
            pause
            exit /b 1
        )
        python -m venv ".venv"
    )
    if errorlevel 1 (
        echo [ERRO] Falha ao criar o ambiente virtual.
        pause
        exit /b 1
    )
    echo [INFO] Instalando dependencias...
    "%VENV_PYTHON%" -m pip install --upgrade pip
    if errorlevel 1 goto :erro_dependencias
    "%VENV_PYTHON%" -m pip install -r requirements.txt
    if errorlevel 1 goto :erro_dependencias
)

if not exist ".env" (
    echo [ERRO] Arquivo .env nao encontrado.
    echo Copie .env.example para .env e configure as credenciais Oracle.
    pause
    exit /b 1
)

echo [INFO] Iniciando importacao...
"%VENV_PYTHON%" main.py
set "APP_EXIT_CODE=%ERRORLEVEL%"
if not "%APP_EXIT_CODE%"=="0" (
    echo [ERRO] A importacao terminou com codigo %APP_EXIT_CODE%. Consulte a pasta logs.
) else (
    echo [INFO] Importacao concluida.
)
pause
exit /b %APP_EXIT_CODE%

:erro_dependencias
echo [ERRO] Nao foi possivel instalar as dependencias. Verifique a conexao de rede e tente novamente.
pause
exit /b 1
