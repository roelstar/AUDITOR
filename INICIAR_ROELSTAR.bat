@echo off
setlocal
chcp 65001 >nul
title ROELSTAR - Diagnostico Financiero Empresarial

cd /d "%~dp0"

echo ================================================
echo   ROELSTAR - Diagnostico Financiero Empresarial
echo ================================================
echo.

REM Verificar que Python este instalado
where py >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=py -3"
    goto python_ok
)

where python >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=python"
    goto python_ok
)

echo ERROR: No se encontro Python instalado.
echo Instala Python 3.10 o superior desde https://www.python.org/downloads/
echo Durante la instalacion, activa la opcion "Add Python to PATH".
echo.
pause
exit /b 1

:python_ok
echo [1/3] Verificando Python...
%PYTHON_CMD% --version
if errorlevel 1 (
    echo ERROR: No se pudo ejecutar Python.
    pause
    exit /b 1
)

if not exist "roelstar_diagnostico_empresarial.py" (
    echo ERROR: No se encontro roelstar_diagnostico_empresarial.py
    echo Asegurate de extraer todos los archivos del ZIP en una carpeta.
    echo No ejecutes este BAT desde la vista previa del archivo comprimido.
    echo.
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ERROR: No se encontro requirements.txt en esta carpeta.
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] Instalando o verificando dependencias...
%PYTHON_CMD% -m pip install --upgrade pip
if errorlevel 1 (
    echo AVISO: No se pudo actualizar pip. Se intentara instalar dependencias igualmente.
)

%PYTHON_CMD% -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: No se pudieron instalar las dependencias.
    echo Verifica tu conexion a Internet y vuelve a ejecutar este archivo.
    echo.
    pause
    exit /b 1
)

echo.
echo [3/3] Iniciando ROELSTAR en el navegador...
%PYTHON_CMD% -m streamlit run roelstar_diagnostico_empresarial.py
if errorlevel 1 (
    echo.
    echo La aplicacion se cerro o no pudo iniciarse.
    echo Revisa los mensajes anteriores para identificar el error.
    echo.
    pause
    exit /b 1
)

echo.
echo La aplicacion se ha detenido.
pause
endlocal
