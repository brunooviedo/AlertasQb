"""
Configuración para servidor de actualizaciones usando GitHub Releases
"""

import os
import json
from pathlib import Path


def setup_github_releases():
    """Configurar GitHub como servidor de actualizaciones"""
    
    print("🔧 CONFIGURACIÓN DE ACTUALIZACIONES VÍA GITHUB")
    print("=" * 50)
    
    # Solicitar información del repositorio
    github_user = input("👤 Tu usuario de GitHub: ")
    repo_name = input("📁 Nombre del repositorio (ej: alertasqb): ")
    github_token = input("🔑 Token de GitHub (opcional, para repos privados): ")
    
    # Actualizar URLs en version.py
    version_file = Path("src/utils/version.py")
    
    with open(version_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # URLs de GitHub
    github_api = f"https://api.github.com/repos/{github_user}/{repo_name}/releases/latest"
    github_repo = f"https://github.com/{github_user}/{repo_name}"
    
    # Reemplazar URLs
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('UPDATE_SERVER_URL = '):
            lines[i] = f'UPDATE_SERVER_URL = "{github_api}"'
        elif line.startswith('GITHUB_REPO = '):
            lines[i] = f'GITHUB_REPO = "{github_repo}"'
    
    with open(version_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print("✅ Configuración actualizada")
    
    # Crear adaptador para GitHub API
    create_github_adapter()
    
    # Instrucciones
    print("\n📝 INSTRUCCIONES PARA USAR GITHUB RELEASES:")
    print("1. Crea un repositorio en GitHub")
    print("2. Sube tu código al repositorio")
    print("3. Usa 'python create_release.py' para generar releases")
    print("4. Los releases se crearán automáticamente en GitHub")


def create_github_adapter():
    """Crear adaptador para GitHub API"""
    
    adapter_content = '''"""
Adaptador para GitHub Releases API
Permite usar GitHub como servidor de actualizaciones
"""

import requests
from src.utils.updater import UpdateChecker


class GitHubUpdateChecker(UpdateChecker):
    """Verifica actualizaciones usando GitHub Releases API"""
    
    def check_for_updates(self):
        """Verifica actualizaciones en GitHub Releases"""
        try:
            print(f"🔍 Verificando actualizaciones en GitHub...")
            
            # GitHub API endpoint
            response = requests.get(self.update_server_url, timeout=self.timeout)
            response.raise_for_status()
            
            release_info = response.json()
            
            latest_version = release_info.get('tag_name', '1.0.0').replace('v', '')
            download_url = None
            
            # Buscar archivo ZIP en los assets
            for asset in release_info.get('assets', []):
                if asset['name'].endswith('.zip'):
                    download_url = asset['browser_download_url']
                    break
            
            if not download_url:
                self.error_occurred.emit("No se encontró archivo de actualización")
                return
            
            changelog = release_info.get('body', 'Sin información de cambios')
            release_date = release_info.get('published_at', 'Desconocida')
            
            print(f"📋 Versión actual: {self.current_version}")
            print(f"📋 Versión disponible: {latest_version}")
            
            # Comparar versiones
            from packaging import version
            if version.parse(latest_version) > version.parse(self.current_version):
                update_info = {
                    'version': latest_version,
                    'download_url': download_url,
                    'changelog': changelog,
                    'release_date': release_date
                }
                print("🆕 Nueva actualización disponible en GitHub!")
                self.update_available.emit(update_info)
            else:
                print("✅ Aplicación actualizada")
                self.no_updates.emit()
                
        except Exception as e:
            print(f"❌ Error al verificar actualizaciones en GitHub: {str(e)}")
            self.error_occurred.emit(f"Error al verificar actualizaciones: {str(e)}")
'''
    
    github_adapter_file = Path("src/utils/github_updater.py")
    with open(github_adapter_file, 'w', encoding='utf-8') as f:
        f.write(adapter_content)
    
    print(f"✅ Adaptador de GitHub creado: {github_adapter_file}")


def main():
    setup_github_releases()


if __name__ == "__main__":
    main()
