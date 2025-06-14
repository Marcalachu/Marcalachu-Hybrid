
#!/usr/bin/env python3
"""
Script para instalar dependencias de PirxcyProxy
Maneja la compatibilidad entre Windows y Linux/Unix
"""

import os
import sys
import subprocess
import platform
import time

def install_requirements():
    """Instala las dependencias desde requirements.txt"""
    try:
        print("🔄 Instalando dependencias...")
        print("   Esto puede tomar unos minutos...")

        # Actualizar pip primero
        print("📦 Actualizando pip...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], check=True, capture_output=True, text=True)

        # Instalar requirements con timeout y mejor manejo
        print("📦 Instalando paquetes...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", 
            "--no-cache-dir", "--timeout", "300"
        ], check=True, capture_output=False, text=True)

        print("✅ Dependencias instaladas correctamente")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        print("🔧 Intentando instalación individual...")
        return install_individually()
    except FileNotFoundError:
        print("❌ No se encontró el archivo requirements.txt")
        return False

def install_individually():
    """Instala cada paquete individualmente"""
    packages = [
        "fade", "pystyle", "mitmproxy", "semver", "survey", 
        "ujson", "crayons", "requests", "console", "pypresence", 
        "rich", "aiohttp", "psutil", "aiofiles"
    ]
    
    failed = []
    for package in packages:
        try:
            print(f"📦 Instalando {package}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", package, "--no-cache-dir"
            ], check=True, capture_output=True, text=True)
            print(f"✅ {package} instalado")
        except subprocess.CalledProcessError:
            print(f"❌ Error instalando {package}")
            failed.append(package)
    
    if failed:
        print(f"❌ Paquetes que fallaron: {', '.join(failed)}")
        return False
    return True

def check_platform_compatibility():
    """Verifica la compatibilidad de la plataforma"""
    current_platform = platform.system()
    print(f"🖥️  Plataforma detectada: {current_platform}")

    if current_platform == "Windows":
        print("✅ Plataforma Windows - winreg disponible")
        return True
    else:
        print("⚠️  Plataforma Unix/Linux - winreg no disponible")
        print("   Se ejecutará en modo compatible (sin funciones de proxy de Windows)")
        create_platform_wrapper()
        return False

def create_platform_wrapper():
    """Crea un wrapper para manejar funciones específicas de Windows"""
    wrapper_content = '''"""
Wrapper para compatibilidad multiplataforma
"""
import platform
import sys

IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    try:
        import winreg
        WINREG_AVAILABLE = True
    except ImportError:
        WINREG_AVAILABLE = False
        winreg = None
else:
    WINREG_AVAILABLE = False
    winreg = None

def proxy_toggle(enable: bool = True):
    """Habilita/deshabilita el proxy del sistema"""
    if not IS_WINDOWS or not WINREG_AVAILABLE:
        status = "habilitado" if enable else "deshabilitado"
        print(f"ℹ️  Proxy {status} (función no disponible en esta plataforma)")
        return

    try:
        INTERNET_SETTINGS = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings",
            0,
            winreg.KEY_ALL_ACCESS,
        )

        def set_key(name: str, value):
            try:
                _, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
                winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type, value)
            except FileNotFoundError:
                winreg.SetValueEx(INTERNET_SETTINGS, name, 0, winreg.REG_SZ, value)

        proxy_enable = winreg.QueryValueEx(INTERNET_SETTINGS, "ProxyEnable")[0]

        if proxy_enable == 0 and enable:
            set_key("ProxyServer", "127.0.0.1:1942")
            set_key("ProxyEnable", 1)
        elif proxy_enable == 1 and not enable:
            set_key("ProxyEnable", 0)
            set_key("ProxyServer", "")

    except Exception as e:
        print(f"❌ Error configurando proxy: {e}")

def gracefulExit():
    """Salida limpia del programa"""
    proxy_toggle(enable=False)
    sys.exit(0)
'''

    with open("platform_compat.py", "w", encoding="utf-8") as f:
        f.write(wrapper_content)

def main():
    print("🚀 PirxcyProxy - Instalador de Dependencias")
    print("=" * 50)

    # Verificar compatibilidad de plataforma
    is_windows = check_platform_compatibility()

    # Instalar dependencias
    if install_requirements():
        print("✅ Instalación completada")
    else:
        print("❌ Error en la instalación")
        print("💡 Intenta ejecutar: pip install --upgrade pip")
        print("💡 Luego ejecuta este script nuevamente")
        return 1

    if not is_windows:
        print("\n📝 En sistemas Linux, modifica main.py para usar:")
        print("   from platform_compat import proxy_toggle, gracefulExit")

    print("\n🎉 ¡Listo para ejecutar PirxcyProxy!")
    print("   Ejecuta: python main.py")

    return 0

if __name__ == "__main__":
    sys.exit(main())
