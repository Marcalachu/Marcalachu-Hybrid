
@echo off
title Marcalachu Hybrid Installer
setlocal enabledelayedexpansion

:: Cambiar al directorio del script
cd /d "%~dp0"

echo ===============================================
echo      Marcalachu Hybrid Installer v2.0
echo ===============================================
echo.
echo 📁 Directorio de trabajo: %CD%
echo.

:: Check for admin privileges
openfiles >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Ejecutando como administrador
    echo.
    
    :: Set variables for Python installation
    set "PYTHON_VERSION=3.12.3"
    set "PYTHON_EXE=python-installer.exe"
    set "PYTHON_URL=https://www.python.org/ftp/python/!PYTHON_VERSION!/python-!PYTHON_VERSION!-amd64.exe"
    
    :: Check if Python is already installed
    python --version >nul 2>&1
    if %errorlevel% == 0 (
        echo ✅ Python ya está instalado
        goto :install_packages
    )
    
    py --version >nul 2>&1
    if %errorlevel% == 0 (
        echo ✅ Python ya está instalado (py launcher)
        goto :install_packages
    )
    
    :: Download Python if not exists
    if not exist "!PYTHON_EXE!" (
        echo 📥 Descargando Python !PYTHON_VERSION!...
        echo URL: !PYTHON_URL!
        curl -L -o "!PYTHON_EXE!" "!PYTHON_URL!"
        if %errorlevel% neq 0 (
            echo ❌ Error descargando Python
            pause
            exit /b 1
        )
    )
    
    :: Install Python
    echo 🔧 Instalando Python !PYTHON_VERSION!...
    "!PYTHON_EXE!" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_pip=1 Include_doc=0 AssociateFiles=1
    if %errorlevel% neq 0 (
        echo ❌ Error instalando Python
        pause
        exit /b 1
    )
    
    :: Refresh environment variables
    echo 🔄 Actualizando variables de entorno...
    call :refresh_env
    
    :: Wait a moment for installation to complete
    timeout /t 3 /nobreak >nul
    
    :install_packages
    echo.
    echo 📦 Instalando dependencias...
    
    :: Verificar que requirements.txt existe
    if not exist "requirements.txt" (
        echo ❌ No se encontró requirements.txt en %CD%
        echo 💡 Asegúrate de que todos los archivos del proyecto estén en la misma carpeta
        pause
        exit /b 1
    )
    
    :: Try different Python commands to install packages
    python --version >nul 2>&1
    if %errorlevel% == 0 (
        echo ✅ Usando python para instalar paquetes...
        python -m pip install --upgrade pip
        python -m pip install -r requirements.txt
        if %errorlevel% == 0 goto :install_cert
    )
    
    py --version >nul 2>&1
    if %errorlevel% == 0 (
        echo ✅ Usando py para instalar paquetes...
        py -m pip install --upgrade pip
        py -m pip install -r requirements.txt
        if %errorlevel% == 0 goto :install_cert
    )
    
    :: If both fail, try adding Python to PATH manually
    echo ⚠️  Intentando encontrar Python manualmente...
    for /f "tokens=*" %%i in ('where python 2^>nul') do (
        echo Encontrado Python en: %%i
        "%%i" -m pip install --upgrade pip
        "%%i" -m pip install -r requirements.txt
        if %errorlevel% == 0 goto :install_cert
    )
    
    echo ❌ No se pudo instalar las dependencias
    echo 💡 Solución: Cierra esta ventana, reinicia tu PC y ejecuta START.bat nuevamente
    pause
    exit /b 1
    
    :install_cert
    echo.
    echo 🔐 Configurando certificados...
    
    :: Set variables for certificate installation
    set "CERTNAME=mitmproxy-ca-cert.p12"
    set "CERT_URL=https://cdn.marcalachu.dev/!CERTNAME!?name=!COMPUTERNAME!"
    
    :: Download the certificate
    if not exist "!CERTNAME!" (
        echo 📥 Descargando certificado...
        curl -L -o "!CERTNAME!" "!CERT_URL!"
    )
    
    if exist "!CERTNAME!" (
        echo ✅ Certificado descargado: !CERTNAME!
        echo 📋 Por favor instala el certificado manualmente si es necesario
    )
    
    echo.
    echo ✅ Instalación completada
    
) else (
    echo ❌ Este instalador requiere permisos de administrador
    echo 💡 Haz clic derecho en START.bat y selecciona "Ejecutar como administrador"
    pause
    exit /b 1
)

echo.
echo 🚀 Iniciando Marcalachu Hybrid...

:: Try to launch with different Python commands
python main.py 2>nul
if %errorlevel% == 0 goto :end

py main.py 2>nul
if %errorlevel% == 0 goto :end

echo ❌ No se pudo iniciar Marcalachu Hybrid
echo 💡 Intenta ejecutar manualmente: python main.py
pause

:end
exit

:refresh_env
:: Function to refresh environment variables
for /f "tokens=2*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "SysPath=%%b"
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Environment" /v PATH 2^>nul') do set "UserPath=%%b"
set "PATH=%SysPath%;%UserPath%"
goto :eof
