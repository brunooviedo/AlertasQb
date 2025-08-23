"""
Script para crear un release en GitHub usando la API REST
Requiere un token de acceso personal de GitHub
"""

import requests
import json
import os
from pathlib import Path


def create_github_release():
    """Crear release en GitHub"""
    
    # Configuración
    REPO_OWNER = "brunooviedo"
    REPO_NAME = "AlertasQb"
    VERSION = "1.2.1"
    TAG_NAME = f"v{VERSION}"
    
    # Token de GitHub (varias fuentes)
    github_token = os.getenv("GITHUB_TOKEN")
    
    # Si no está en variables de entorno, intentar leer desde .env
    if not github_token:
        env_file = Path(".env")
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith("GITHUB_TOKEN="):
                        github_token = line.split("=", 1)[1].strip()
                        break
    
    if not github_token:
        print("❌ Error: Necesitas configurar un token de GitHub")
        print("Opción 1 (Recomendada): $env:GITHUB_TOKEN='tu_token_aqui'")
        print("Opción 2: Edita el archivo .env y pon: GITHUB_TOKEN=tu_token_aqui")
        print("Opción 3: Ve a GitHub Settings > Developer settings > Personal access tokens")
        return False
    
    # Headers para la API (formato simplificado)
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }
    
    # Datos del release
    release_data = {
        "tag_name": TAG_NAME,
        "target_commitish": "main",
        "name": f"AlertasQB v{VERSION}",
        "body": f"""# AlertasQB v{VERSION}

## 🚀 Características principales

- ✅ **Sistema de actualizaciones automáticas**: Verificación automática desde GitHub
- ✅ **Dashboard mejorado**: Gráficos con colores por tipo de alerta
- ✅ **Gestión de usuarios**: Sistema completo de autenticación
- ✅ **Importación Excel**: Soporte completo para datos geotécnicos
- ✅ **Base de datos**: Almacenamiento persistente con SQLite

## 🔧 Instalación

1. Descarga el archivo `AlertasQB-v{VERSION}.zip`
2. Extrae el contenido en una carpeta
3. Ejecuta `AlertasQB.exe`

## 📝 Cambios en esta versión

- Sistema completo de actualizaciones automáticas
- Configuración con GitHub para releases
- Interfaz mejorada del dashboard
- Optimizaciones de rendimiento

## 🐛 Reportar problemas

Si encuentras algún problema, por favor [crea un issue](https://github.com/{REPO_OWNER}/{REPO_NAME}/issues/new).

## 📞 Soporte

- **Email**: bruno@alertasqb.com
- **Repositorio**: https://github.com/{REPO_OWNER}/{REPO_NAME}
""",
        "draft": False,
        "prerelease": False,
        "generate_release_notes": True
    }
    
    # URL de la API
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
    
    print(f"🚀 Creando release {TAG_NAME} en GitHub...")
    print(f"🔗 URL: {url}")
    print(f"🔑 Token length: {len(github_token)}")
    
    # Crear el release
    response = requests.post(url, headers=headers, json=release_data)
    
    if response.status_code == 201:
        release_info = response.json()
        print(f"✅ Release creado exitosamente!")
        print(f"🔗 URL: {release_info['html_url']}")
        print(f"📄 Upload URL: {release_info['upload_url']}")
        
        # Subir el archivo ZIP si existe
        zip_file = Path(f"releases/AlertasQB-v{VERSION}.zip")
        if zip_file.exists():
            upload_asset(release_info['upload_url'], zip_file, headers)
        else:
            print(f"⚠️  No se encontró el archivo {zip_file}")
            print("   Puedes subirlo manualmente desde la web de GitHub")
        
        return True
    else:
        print(f"❌ Error al crear release: {response.status_code}")
        print(f"Respuesta: {response.text}")
        return False


def upload_asset(upload_url_template, file_path, headers):
    """Subir archivo al release"""
    # La URL template incluye {?name,label} que necesitamos reemplazar
    upload_url = upload_url_template.replace("{?name,label}", f"?name={file_path.name}")
    
    print(f"📤 Subiendo {file_path.name}...")
    
    # Headers específicos para upload
    upload_headers = headers.copy()
    upload_headers["Content-Type"] = "application/zip"
    
    with open(file_path, 'rb') as f:
        response = requests.post(upload_url, headers=upload_headers, data=f)
    
    if response.status_code == 201:
        print(f"✅ Archivo {file_path.name} subido exitosamente!")
    else:
        print(f"❌ Error al subir {file_path.name}: {response.status_code}")
        print(f"Respuesta: {response.text}")


if __name__ == "__main__":
    create_github_release()
