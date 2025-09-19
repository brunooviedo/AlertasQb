"""
Sistema de Auto-Actualización
Verifica y descarga actualizaciones automáticamente desde un servidor remoto
"""

import json
import os
import sys
import shutil
import zipfile
import tempfile
import subprocess
import threading
from pathlib import Path
from datetime import datetime
import requests
from packaging import version
from PySide6.QtCore import QObject, Signal, QThread, QTimer
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QProgressBar, QPushButton, QTextEdit, QMessageBox)


class UpdateChecker(QObject):
    """Verifica actualizaciones en segundo plano"""
    update_available = Signal(dict)  # Señal cuando hay actualización disponible
    no_updates = Signal()  # Señal cuando no hay actualizaciones
    error_occurred = Signal(str)  # Señal cuando hay error
    
    def __init__(self, update_server_url, current_version, parent=None):
        super().__init__(parent)
        self.update_server_url = update_server_url
        self.current_version = current_version
        self.timeout = 10  # Timeout de 10 segundos
    
    def check_for_updates(self):
        """Verifica si hay actualizaciones disponibles"""
        try:
            # Preparar headers para autenticación (repositorio privado)
            headers = {}
            
            # Si hay token de GitHub, usarlo para repos privados
            github_token = os.getenv("GITHUB_TOKEN")
            if not github_token:
                # Intentar leer desde .env
                env_file = Path(".env")
                if env_file.exists():
                    with open(env_file, 'r') as f:
                        for line in f:
                            if line.startswith("GITHUB_TOKEN="):
                                github_token = line.split("=", 1)[1].strip()
                                break
            
            if github_token:
                headers["Authorization"] = f"Bearer {github_token}"
                headers["Accept"] = "application/vnd.github+json"
            
            # Si es una URL de GitHub API, usar directamente la API
            if "api.github.com" in self.update_server_url:
                version_url = self.update_server_url
            else:
                version_url = f"{self.update_server_url}/version.json"
            
            print(f"🔍 Verificando actualizaciones en: {version_url}")
            print(f"🔧 DEBUG - update_server_url: {self.update_server_url}")
            print(f"🔧 DEBUG - current_version: {self.current_version}")
            
            # Realizar petición HTTP con timeout y headers
            response = requests.get(version_url, timeout=self.timeout, headers=headers)
            response.raise_for_status()
            
            # Si es la API de GitHub, extraer información del release
            if "api.github.com" in self.update_server_url:
                release_info = response.json()
                version_info = {
                    'version': release_info.get('tag_name', '1.0.0').lstrip('v'),
                    'download_url': release_info.get('assets', [{}])[0].get('browser_download_url', ''),
                    'changelog': release_info.get('body', 'Sin información de cambios'),
                    'release_date': release_info.get('published_at', 'Desconocida')
                }
            else:
                version_info = response.json()
            
            latest_version = version_info.get('version', '1.0.0')
            download_url = version_info.get('download_url', '')
            changelog = version_info.get('changelog', 'Sin información de cambios')
            release_date = version_info.get('release_date', 'Desconocida')
            
            print(f"📋 Versión actual: {self.current_version}")
            print(f"📋 Versión disponible: {latest_version}")
            
            # Comparar versiones usando packaging.version
            if version.parse(latest_version) > version.parse(self.current_version):
                update_info = {
                    'version': latest_version,
                    'download_url': download_url,
                    'changelog': changelog,
                    'release_date': release_date
                }
                print("🆕 Nueva actualización disponible!")
                self.update_available.emit(update_info)
            else:
                print("✅ Aplicación actualizada")
                self.no_updates.emit()
                
        except requests.exceptions.Timeout:
            print("⚠️ Timeout al verificar actualizaciones")
            self.error_occurred.emit("Timeout al conectar con el servidor de actualizaciones")
        except requests.exceptions.ConnectionError:
            print("⚠️ Error de conexión al verificar actualizaciones")
            self.error_occurred.emit("No se pudo conectar al servidor de actualizaciones")
        except Exception as e:
            print(f"❌ Error al verificar actualizaciones: {str(e)}")
            self.error_occurred.emit(f"Error al verificar actualizaciones: {str(e)}")


class UpdateDownloader(QThread):
    """Descarga actualizaciones en segundo plano"""
    progress_changed = Signal(int)  # Progreso de descarga (0-100)
    download_completed = Signal(str)  # Ruta del archivo descargado
    download_failed = Signal(str)  # Error en descarga
    
    def __init__(self, download_url, parent=None):
        super().__init__(parent)
        self.download_url = download_url
        self.temp_dir = tempfile.mkdtemp()
    
    def run(self):
        """Descarga la actualización"""
        try:
            print(f"⬇️ Descargando actualización desde: {self.download_url}")
            
            response = requests.get(self.download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            update_file = os.path.join(self.temp_dir, 'update.zip')
            
            with open(update_file, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        
                        if total_size > 0:
                            progress = int((downloaded_size / total_size) * 100)
                            self.progress_changed.emit(progress)
            
            print("✅ Descarga completada")
            self.download_completed.emit(update_file)
            
        except Exception as e:
            print(f"❌ Error en descarga: {str(e)}")
            self.download_failed.emit(str(e))


class UpdateDialog(QDialog):
    """Dialog para mostrar progreso de actualización"""
    
    def __init__(self, update_info, parent=None):
        super().__init__(parent)
        self.update_info = update_info
        self.setup_ui()
        self.downloader = None
        
    def setup_ui(self):
        """Configurar interfaz"""
        self.setWindowTitle("Actualización Disponible - AlertasQB")
        self.setFixedSize(500, 350)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Información de la actualización
        info_label = QLabel(f"🆕 Nueva versión disponible: v{self.update_info['version']}")
        info_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #3153E4; padding: 10px;")
        layout.addWidget(info_label)
        
        # Fecha de lanzamiento
        date_label = QLabel(f"📅 Fecha: {self.update_info['release_date']}")
        layout.addWidget(date_label)
        
        # Changelog
        changelog_label = QLabel("📋 Novedades:")
        changelog_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(changelog_label)
        
        self.changelog_text = QTextEdit()
        self.changelog_text.setPlainText(self.update_info['changelog'])
        self.changelog_text.setMaximumHeight(150)
        self.changelog_text.setReadOnly(True)
        layout.addWidget(self.changelog_text)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel()
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.update_button = QPushButton("🔄 Actualizar Ahora")
        self.update_button.setStyleSheet("""
            QPushButton {
                background-color: #3153E4;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2844CC;
            }
        """)
        self.update_button.clicked.connect(self.start_update)
        
        self.later_button = QPushButton("⏰ Más Tarde")
        self.later_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.later_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.later_button)
        button_layout.addWidget(self.update_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def start_update(self):
        """Iniciar proceso de actualización"""
        self.update_button.setEnabled(False)
        self.later_button.setEnabled(False)
        
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.progress_label.setText("Descargando actualización...")
        
        # Iniciar descarga
        self.downloader = UpdateDownloader(self.update_info['download_url'])
        self.downloader.progress_changed.connect(self.update_progress)
        self.downloader.download_completed.connect(self.on_download_completed)
        self.downloader.download_failed.connect(self.on_download_failed)
        self.downloader.start()
    
    def update_progress(self, progress):
        """Actualizar barra de progreso"""
        self.progress_bar.setValue(progress)
        self.progress_label.setText(f"Descargando actualización... {progress}%")
    
    def on_download_completed(self, file_path):
        """Cuando la descarga se completa"""
        self.progress_label.setText("Instalando actualización...")
        self.progress_bar.setValue(100)
        
        try:
            # Instalar actualización
            self.install_update(file_path)
            
            # Mostrar mensaje de éxito
            QMessageBox.information(self, "Actualización Completada", 
                                  "✅ La actualización se instaló correctamente.\n"
                                  "La aplicación se reiniciará ahora.")
            
            # Reiniciar aplicación
            self.restart_application()
            
        except Exception as e:
            self.on_download_failed(f"Error al instalar: {str(e)}")
    
    def on_download_failed(self, error):
        """Cuando la descarga falla - ofrecer descarga manual"""
        # Crear mensaje personalizado con enlace de descarga manual
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("⚠️ Error de Descarga Automática")
        
        # Estilos para el mensaje
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                min-width: 500px;
            }
            QMessageBox QLabel {
                background-color: white;
                color: #2c3e50;
                padding: 15px;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #3153E4,
                    stop: 1 #1a237e
                );
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 25px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
                margin: 5px;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #1a237e,
                    stop: 1 #0d1142
                );
            }
        """)
        
        # Detectar tipo de error para mejor mensaje
        error_lower = error.lower()
        if any(keyword in error_lower for keyword in ['ssl', 'certificate', 'cert']):
            error_type = "🔒 Certificados SSL bloqueados"
            suggestion = "Su firewall o antivirus está bloqueando conexiones seguras."
        elif any(keyword in error_lower for keyword in ['network', 'connection', 'timeout']):
            error_type = "🌐 Problema de conexión"
            suggestion = "Verifique su conexión a Internet o proxy corporativo."
        elif any(keyword in error_lower for keyword in ['403', 'forbidden', 'unauthorized']):
            error_type = "🚫 Acceso restringido"
            suggestion = "El servidor está bloqueando la descarga automática."
        else:
            error_type = "⚠️ Error de descarga"
            suggestion = "La descarga automática no se pudo completar."
        
        # Construir URL de descarga manual
        download_url = self.update_info.get('download_url', '')
        if not download_url:
            # Generar URL del release de GitHub
            version = self.update_info.get('version', 'latest')
            download_url = f"https://github.com/brunooviedo/AlertasQb/releases/tag/v{version}"
        
        # Mensaje principal
        msg.setText(f"<h2 style='color: #FF9040; margin-bottom: 15px;'>{error_type}</h2>")
        
        # Información detallada
        msg.setInformativeText(f"""
            <p style='color: #2c3e50; font-size: 14px; margin: 10px 0;'>
                <strong>Problema:</strong> {suggestion}
            </p>
            
            <p style='color: #2c3e50; font-size: 14px; margin: 15px 0;'>
                <strong>📥 Descarga Manual:</strong>
            </p>
            
            <p style='background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 10px 0;'>
                <strong>1.</strong> Abra su navegador web<br>
                <strong>2.</strong> Visite: <a href="{download_url}" style="color: #3153E4; text-decoration: none;">
                <code style="background: #e9ecef; padding: 2px 5px; border-radius: 3px;">{download_url}</code></a><br>
                <strong>3.</strong> Descargue el archivo <code>AlertasQB-Standalone-v{self.update_info.get('version', 'latest')}.zip</code><br>
                <strong>4.</strong> Extraiga y ejecute <code>AlertasQB.exe</code>
            </p>
            
            <p style='color: #6c757d; font-size: 12px; margin: 15px 0 5px 0;'>
                <strong>Error técnico:</strong> {error}
            </p>
        """)
        
        # Botones personalizados
        copy_button = msg.addButton("📋 Copiar", QMessageBox.ActionRole)
        open_button = msg.addButton("🌐 Navegador", QMessageBox.ActionRole)
        close_button = msg.addButton("Cerrar", QMessageBox.RejectRole)
        
        # Ejecutar diálogo
        reply = msg.exec()
        
        # Manejar acciones del usuario
        if msg.clickedButton() == copy_button:
            # Copiar URL al portapapeles
            try:
                from PySide6.QtGui import QClipboard
                from PySide6.QtWidgets import QApplication
                clipboard = QApplication.clipboard()
                clipboard.setText(download_url)
                
                # Confirmar que se copió
                QMessageBox.information(self, "✅ Enlace Copiado", 
                                      f"El enlace de descarga se copió al portapapeles:\n\n{download_url}")
            except Exception as e:
                QMessageBox.warning(self, "Error al Copiar", 
                                  f"No se pudo copiar el enlace: {str(e)}")
        
        elif msg.clickedButton() == open_button:
            # Abrir URL en el navegador
            try:
                import webbrowser
                webbrowser.open(download_url)
                QMessageBox.information(self, "🌐 Navegador Abierto", 
                                      "Se abrió la página de descarga en su navegador.")
            except Exception as e:
                QMessageBox.warning(self, "Error al Abrir", 
                                  f"No se pudo abrir el navegador: {str(e)}")
        
        # Cerrar el diálogo de actualización
        self.reject()
    
    def install_update(self, update_file):
        """Instalar la actualización"""
        print("📦 Instalando actualización...")
        
        # Obtener directorio de la aplicación
        if getattr(sys, 'frozen', False):
            # Si es ejecutable
            app_dir = Path(sys.executable).parent
        else:
            # Si es script
            app_dir = Path(__file__).parent.parent.parent
        
        # Crear backup del ejecutable actual
        backup_dir = app_dir / "backup"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Extraer actualización
        temp_extract = tempfile.mkdtemp()
        with zipfile.ZipFile(update_file, 'r') as zip_ref:
            zip_ref.extractall(temp_extract)
        
        # Buscar carpeta de la aplicación en el zip
        extracted_folders = [f for f in os.listdir(temp_extract) if os.path.isdir(os.path.join(temp_extract, f))]
        if extracted_folders:
            source_dir = os.path.join(temp_extract, extracted_folders[0])
        else:
            source_dir = temp_extract
        
        # Hacer backup de archivos importantes
        important_files = ['data', 'config']
        for file_name in important_files:
            src_path = app_dir / file_name
            if src_path.exists():
                backup_path = backup_dir / f"{file_name}_{timestamp}"
                if src_path.is_dir():
                    shutil.copytree(src_path, backup_path)
                else:
                    shutil.copy2(src_path, backup_path)
        
        # Reemplazar archivos
        for item in os.listdir(source_dir):
            src_item = os.path.join(source_dir, item)
            dst_item = app_dir / item
            
            # No reemplazar datos y configuración
            if item in ['data', 'config']:
                continue
                
            if os.path.isdir(src_item):
                if dst_item.exists():
                    shutil.rmtree(dst_item)
                shutil.copytree(src_item, dst_item)
            else:
                if dst_item.exists():
                    dst_item.unlink()
                shutil.copy2(src_item, dst_item)
        
        print("✅ Actualización instalada correctamente")
    
    def restart_application(self):
        """Reiniciar la aplicación"""
        if getattr(sys, 'frozen', False):
            # Si es ejecutable
            subprocess.Popen([sys.executable])
        else:
            # Si es script
            subprocess.Popen([sys.executable, sys.argv[0]])
        
        # Cerrar aplicación actual
        sys.exit(0)


class AutoUpdater(QObject):
    """Clase principal del sistema de actualización"""
    
    def __init__(self, update_server_url, app_version, parent=None):
        super().__init__(parent)
        self.app_version = app_version
        self.update_server_url = update_server_url
        self.parent_widget = parent
        
    def check_for_updates_on_startup(self):
        """Verificar actualizaciones al iniciar (en segundo plano)"""
        self.checker = UpdateChecker(self.update_server_url, self.app_version)
        self.checker.update_available.connect(self.show_update_dialog)
        self.checker.error_occurred.connect(self.handle_update_error)
        
        # Ejecutar verificación en un timer para no bloquear el inicio
        QTimer.singleShot(5000, self.checker.check_for_updates)  # Esperar 5 segundos
    
    def show_update_dialog(self, update_info):
        """Mostrar dialog de actualización"""
        dialog = UpdateDialog(update_info, self.parent_widget)
        dialog.exec()
    
    def handle_update_error(self, error_message):
        """Manejar errores de actualización silenciosamente"""
        print(f"⚠️ Error de actualización (silencioso): {error_message}")
        # No mostrar error al usuario para no interrumpir el flujo
