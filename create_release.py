"""
Script de Release Automático
Genera una nueva versión, la empaqueta y crea los archivos de actualización
"""

import os
import json
import zipfile
import shutil
import subprocess
import argparse
from pathlib import Path
from datetime import datetime


def get_current_version():
    """Obtener versión actual del archivo version.py"""
    version_file = Path("src/utils/version.py")
    if not version_file.exists():
        return "1.0.0"
    
    with open(version_file, 'r', encoding='utf-8') as f:
        content = f.read()
        for line in content.split('\n'):
            if line.startswith('APP_VERSION = '):
                return line.split('"')[1]
    return "1.0.0"


def update_version(new_version):
    """Actualizar versión en el archivo version.py"""
    version_file = Path("src/utils/version.py")
    
    with open(version_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar la línea de versión
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('APP_VERSION = '):
            lines[i] = f'APP_VERSION = "{new_version}"'
            break
    
    with open(version_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Versión actualizada a {new_version}")


def build_executable():
    """Compilar el ejecutable usando PyInstaller"""
    print("🔨 Compilando ejecutable...")
    
    # Activar entorno virtual y compilar
    cmd = [
        "powershell", "-Command",
        "cd 'C:\\Users\\Bruno\\Desktop\\BD alertas' ; "
        ".\\venv\\Scripts\\Activate.ps1 ; "
        "pyinstaller AlertasQB.spec --clean --noconfirm"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Compilación exitosa")
        return True
    else:
        print(f"❌ Error en compilación: {result.stderr}")
        return False


def create_release_package(version, changelog):
    """Crear paquete de release"""
    print(f"📦 Creando paquete v{version}...")
    
    # Directorio de distribución
    dist_dir = Path("dist/AlertasQB")
    if not dist_dir.exists():
        print("❌ No se encontró el directorio dist/AlertasQB")
        return None
    
    # Crear directorio de releases
    release_dir = Path("releases")
    release_dir.mkdir(exist_ok=True)
    
    # Nombre del archivo de release
    release_name = f"AlertasQB-v{version}.zip"
    release_path = release_dir / release_name
    
    # Crear ZIP con el contenido de dist/AlertasQB
    with zipfile.ZipFile(release_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in dist_dir.rglob('*'):
            if file_path.is_file():
                arcname = f"AlertasQB/{file_path.relative_to(dist_dir)}"
                zipf.write(file_path, arcname)
    
    # Crear archivo de versión para el servidor
    version_info = {
        "version": version,
        "download_url": f"https://tu-servidor.com/releases/{release_name}",
        "changelog": changelog,
        "release_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file_size": release_path.stat().st_size,
        "checksum": "sha256_here"  # Puedes calcular SHA256 si lo necesitas
    }
    
    version_json_path = release_dir / "version.json"
    with open(version_json_path, 'w', encoding='utf-8') as f:
        json.dump(version_info, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Release creado: {release_path}")
    print(f"📄 Archivo de versión: {version_json_path}")
    
    return release_path, version_json_path


def increment_version(current_version, increment_type="patch"):
    """Incrementar versión automáticamente"""
    parts = current_version.split('.')
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    
    if increment_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif increment_type == "minor":
        minor += 1
        patch = 0
    else:  # patch
        patch += 1
    
    return f"{major}.{minor}.{patch}"


def main():
    """Función principal del script de release"""
    parser = argparse.ArgumentParser(description="Generar release de AlertasQB")
    parser.add_argument("--version", help="Versión específica (ej: 1.2.3)")
    parser.add_argument("--increment", choices=["major", "minor", "patch"], 
                       default="patch", help="Tipo de incremento automático")
    parser.add_argument("--changelog", help="Descripción de cambios")
    parser.add_argument("--no-build", action="store_true", help="No compilar, solo empaquetar")
    
    args = parser.parse_args()
    
    print("🚀 Iniciando proceso de release...")
    
    # Obtener versión actual
    current_version = get_current_version()
    print(f"📋 Versión actual: {current_version}")
    
    # Determinar nueva versión
    if args.version:
        new_version = args.version
    else:
        new_version = increment_version(current_version, args.increment)
    
    print(f"🆕 Nueva versión: {new_version}")
    
    # Actualizar versión en código
    update_version(new_version)
    
    # Compilar ejecutable (si no se especifica --no-build)
    if not args.no_build:
        if not build_executable():
            print("❌ Error en compilación, abortando release")
            return
    
    # Obtener changelog
    changelog = args.changelog or input("📝 Ingrese descripción de cambios: ")
    if not changelog:
        changelog = f"Actualización v{new_version}"
    
    # Crear paquete de release
    release_files = create_release_package(new_version, changelog)
    
    if release_files:
        release_path, version_json = release_files
        print("\n🎉 RELEASE COMPLETADO!")
        print(f"📦 Archivo: {release_path}")
        print(f"📄 Versión JSON: {version_json}")
        print(f"📏 Tamaño: {release_path.stat().st_size / 1024 / 1024:.2f} MB")
        print("\n📝 Próximos pasos:")
        print("1. Subir el archivo ZIP a tu servidor")
        print("2. Subir version.json a tu servidor de actualizaciones")
        print("3. Actualizar la URL del servidor en src/utils/version.py")
    else:
        print("❌ Error al crear release")


if __name__ == "__main__":
    main()
