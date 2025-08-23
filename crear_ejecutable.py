"""
Script para crear ejecutable independiente de AlertasQB
Genera un archivo .exe que incluye Python y todas las dependencias
"""

import os
import subprocess
import sys
from pathlib import Path

def create_standalone_exe():
    """Crear ejecutable independiente"""
    
    print("🚀 Creando ejecutable independiente de AlertasQB...")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not Path("main.py").exists():
        print("❌ Error: Ejecuta este script desde la carpeta raíz del proyecto")
        return False
    
    # Comando PyInstaller optimizado
    cmd = [
        "pyinstaller",
        "--onedir",  # Un directorio (más rápido de ejecutar)
        "--windowed",  # Sin ventana de consola
        "--name=AlertasQB",
        "--icon=assets/icon.ico" if Path("assets/icon.ico").exists() else "",
        "--add-data=config;config",  # Incluir carpeta config
        "--add-data=data;data",      # Incluir carpeta data
        "--add-data=src;src",        # Incluir código fuente
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtGui", 
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        "--hidden-import=openpyxl",
        "--hidden-import=requests",
        "--hidden-import=bcrypt",
        "--clean",
        "--noconfirm",
        "main.py"
    ]
    
    # Filtrar elementos vacíos
    cmd = [arg for arg in cmd if arg]
    
    print("🔨 Comando PyInstaller:")
    print(" ".join(cmd))
    print()
    
    # Ejecutar PyInstaller
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Ejecutable creado exitosamente!")
        
        # Verificar que se creó
        exe_path = Path("dist/AlertasQB/AlertasQB.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / 1024 / 1024
            print(f"📦 Archivo: {exe_path}")
            print(f"📏 Tamaño: {size_mb:.1f} MB")
            
            # Crear paquete de distribución
            create_distribution_package()
            
        else:
            print("❌ No se encontró el ejecutable generado")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando PyInstaller:")
        print(f"Salida: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False
    
    return True

def create_distribution_package():
    """Crear paquete de distribución completo"""
    print("\n📦 Creando paquete de distribución...")
    
    import zipfile
    import shutil
    
    # Directorio de distribución
    dist_dir = Path("dist/AlertasQB")
    if not dist_dir.exists():
        print("❌ No se encontró el directorio de distribución")
        return
    
    # Crear carpeta de release si no existe
    release_dir = Path("releases")
    release_dir.mkdir(exist_ok=True)
    
    # Nombre del paquete
    from src.utils.version import APP_VERSION
    package_name = f"AlertasQB-Standalone-v{APP_VERSION}.zip"
    package_path = release_dir / package_name
    
    # Crear ZIP
    with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Añadir todo el contenido de dist/AlertasQB
        for file_path in dist_dir.rglob('*'):
            if file_path.is_file():
                arcname = f"AlertasQB/{file_path.relative_to(dist_dir)}"
                zipf.write(file_path, arcname)
        
        # Añadir documentación
        docs = ["README.md", "INSTALACION.md", "SISTEMA_ACTUALIZACION.md"]
        for doc in docs:
            if Path(doc).exists():
                zipf.write(doc, f"AlertasQB/{doc}")
    
    size_mb = package_path.stat().st_size / 1024 / 1024
    print(f"✅ Paquete creado: {package_path}")
    print(f"📏 Tamaño: {size_mb:.1f} MB")
    print(f"\n🎯 Para distribuir:")
    print(f"1. Comparte el archivo: {package_name}")
    print(f"2. El usuario extrae y ejecuta AlertasQB.exe")
    print(f"3. ¡No necesita instalar Python ni dependencias!")

def main():
    """Función principal"""
    print("AlertasQB - Generador de Ejecutable Independiente")
    print("=" * 60)
    
    # Verificar PyInstaller
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📥 Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller instalado")
    
    # Crear ejecutable
    if create_standalone_exe():
        print("\n🎉 ¡Proceso completado exitosamente!")
        print("\n📋 Próximos pasos:")
        print("1. Prueba el ejecutable en dist/AlertasQB/AlertasQB.exe")
        print("2. Comparte el ZIP generado en releases/")
        print("3. Los usuarios solo necesitan extraer y ejecutar")
    else:
        print("\n❌ Proceso falló. Revisa los errores arriba.")

if __name__ == "__main__":
    main()
