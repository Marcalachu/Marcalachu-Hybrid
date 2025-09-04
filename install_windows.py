#!/usr/bin/env python3
"""
Instalador de dependencias para Marcalachu hybrid en Windows
"""

import os
import sys
import subprocess
import platform

def check_python():
    """Verifica que Python esté instalado correctamente"""
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor} es muy antiguo. Se requiere Python 3.8+")
            return False
    except Exception as e:
        print(f"❌ Error verificando Python: {e}")
        return False

def check_pip():
    """Verifica que pip esté disponible"""
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✅ pip disponible: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("❌ pip no está disponible")
        return False
    except FileNotFoundError:
        print("❌ pip no se encuentra en el sistema")
        return False

def install_requirements():
    """Instala las dependencias desde requirements.txt"""
    if not os.path.exists("requirements.txt"):
        print("❌ No se encontró requirements.txt")
        return False
    
    try:
        print("🔄 Instalando dependencias desde requirements.txt...")
        
        # Actualizar pip primero
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True)
        
        # Instalar dependencias
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--user"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Dependencias instaladas correctamente")
        if result.stdout:
            print(f"Salida: {result.stdout}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        if e.stderr:
            print(f"Error detallado: {e.stderr}")
        
        # Intentar instalar una por una si falla la instalación masiva
        print("🔄 Intentando instalación individual de paquetes...")
        return install_individual_packages()
    
def install_individual_packages():
    """Instala paquetes individualmente si la instalación masiva falla"""
    packages = [
        "fade", "pystyle", "mitmproxy", "semver", "survey", 
        "ujson", "crayons", "requests", "console", "pypresence", 
        "rich", "aiohttp", "psutil", "aiofiles"
    ]
    
    failed_packages = []
    
    for package in packages:
        try:
            print(f"📦 Instalando {package}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", package, "--user"
            ], check=True, capture_output=True)
            print(f"✅ {package} instalado")
        except subprocess.CalledProcessError as e:
            print(f"❌ Falló la instalación de {package}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n❌ Paquetes que fallaron: {', '.join(failed_packages)}")
        print("💡 Intenta instalarlos manualmente con:")
        for pkg in failed_packages:
            print(f"   pip install {pkg}")
        return False
    
    return True

def create_launcher():
    """Crea un launcher mejorado para Windows"""
    launcher_content = '''@echo off
title Marcalachu Hybrid
cd /d "%~dp0"

echo 🚀 Iniciando Marcalachu hybrid...
echo.

REM Verificar si Python está disponible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado o no está en el PATH
    echo 💡 Descarga Python desde https://python.org
    pause
    exit /b 1
)

REM Ejecutar el programa principal
python main.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ El programa terminó con errores
    pause
)
'''
    
    with open("run_Ejecuta Hybrid.py", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print("✅ Launcher creado: run_pirxcy.bat")

def main():
    print("🚀 Marcalachu Hybrid - Instalador para Windows")
    print("=" * 50)
    
    # Verificar que estamos en Windows
    if platform.system() != "Windows":
        print("⚠️  Este instalador está diseñado para Windows")
        print("   En otros sistemas, usa: python instal_dependencies.py")
        return 1
    
    # Verificaciones básicas
    if not check_python():
        print("\n💡 Solución:")
        print("   1. Descarga Python desde https://python.org")
        print("   2. Durante la instalación, marca 'Add Python to PATH'")
        print("   3. Reinicia la terminal y ejecuta este script nuevamente")
        input("\nPresiona Enter para continuar...")
        return 1
    
    if not check_pip():
        print("\n💡 Solución:")
        print("   1. Reinstala Python asegurándote de incluir pip")
        print("   2. O ejecuta: python -m ensurepip --upgrade")
        input("\nPresiona Enter para continuar...")
        return 1
    
    # Instalar dependencias
    if install_requirements():
        print("\n✅ Instalación completada exitosamente")
        create_launcher()
        
        print("\n🎉 ¡Todo listo!")
        print("📋 Para ejecutar PirxcyProxy:")
        print("   • Doble clic en run_pirxcy.bat")
        print("   • O ejecuta: python main.py")
        
    else:
        print("\n❌ La instalación falló")
        print("💡 Posibles soluciones:")
        print("   1. Ejecuta como Administrador")
        print("   2. Verifica tu conexión a internet")
        print("   3. Actualiza pip: python -m pip install --upgrade pip")
    
    input("\nPresiona Enter para continuar...")
    return 0

if __name__ == "__main__":
    sys.exit(main())
