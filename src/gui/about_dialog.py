#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diálogo "Acerca de..." para el Sistema de Alertas Geotécnicas
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap

# Importar estilos centralizados
from src.gui.styles import DialogStyles
# Importar versión actual
from src.utils.version import APP_VERSION

class AboutDialog(QDialog):
    """Diálogo personalizado para mostrar información sobre la aplicación"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de Sistema de Alertas Geotécnicas")
        self.setFixedSize(500, 450)
        self.setModal(True)
        
        # Aplicar estilos centralizados
        self.setStyleSheet(DialogStyles.get_complete_dialog_styles())
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título principal
        title_label = QLabel("Sistema de Alertas Geotécnicas")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setProperty("aboutTitle", True)  # Usar propiedad CSS
        layout.addWidget(title_label)
        
        # Versión
        version_label = QLabel(f"Versión {APP_VERSION}")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setProperty("aboutVersion", True)  # Usar propiedad CSS
        layout.addWidget(version_label)
        
        # Descripción y características
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(220)
        info_text.setProperty("aboutInfo", True)  # Usar propiedad CSS
        
        info_content = """
        <p><b>Descripción:</b><br>
        Aplicación para el registro, seguimiento y análisis de alertas geotécnicas con interfaz intuitiva y herramientas de visualización avanzadas.</p>
        
        <p><b>Características principales:</b></p>
        <ul style="margin-left: 20px;">
        <li>📊 Dashboard interactivo con gráficos en tiempo real</li>
        <li>🚨 Registro de alertas con clasificación por colores (Roja, Amarilla, Naranja)</li>
        <li>📈 Análisis y filtrado de datos por año, mes y tipo de alerta</li>
        <li>📁 Importación/Exportación de datos Excel</li>
        <li>👤 Sistema de autenticación y gestión de usuarios</li>
        <li>🗄️ Integración con bases de datos SQL Server</li>
        <li>🔍 Herramientas de búsqueda y filtrado avanzado</li>
        </ul>
        
        <p><b>Tecnologías utilizadas:</b><br>
        Python 3.12, PySide6, Pandas, Matplotlib, OpenPyXL</p>
        """
        
        info_text.setHtml(info_content)
        layout.addWidget(info_text)
        
        # Información del desarrollador
        developer_label = QLabel("Desarrollado por: <b>Bruno Oviedo</b> © 2025")
        developer_label.setAlignment(Qt.AlignCenter)
        developer_label.setProperty("aboutDeveloper", True)  # Usar propiedad CSS
        layout.addWidget(developer_label)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        # Botón de verificar actualizaciones
        update_button = QPushButton("🔄 Verificar Actualizaciones")
        update_button.setFixedSize(220, 35)
        update_button.setProperty("aboutUpdate", True)  # Usar propiedad CSS
        update_button.clicked.connect(self.check_for_updates)
        
        # Botón de cerrar
        close_button = QPushButton("Cerrar")
        close_button.setFixedSize(100, 35)
        close_button.setProperty("aboutClose", True)  # Usar propiedad CSS
        close_button.clicked.connect(self.accept)
        
        button_layout.addStretch()
        button_layout.addWidget(update_button)
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
    def check_for_updates(self):
        """Verificar actualizaciones manualmente desde el diálogo About"""
        try:
            from PySide6.QtWidgets import QMessageBox
            from PySide6.QtCore import QTimer
            from src.utils.updater import UpdateChecker
            from src.utils.version import UPDATE_SERVER_URL
            
            # Cambiar texto del botón mientras verifica
            sender = self.sender()
            original_text = sender.text()
            sender.setText("⏳ Verificando...")
            sender.setEnabled(False)
            
            # Cambiar color del botón mientras verifica (naranja)
            sender.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #FF9040,
                        stop: 1 #E67E22
                    );
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 12px 20px;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    min-width: 180px;
                }
            """)
            
            # Procesar eventos para mostrar el cambio
            from PySide6.QtWidgets import QApplication
            QApplication.processEvents()
            
            # Verificar actualizaciones
            checker = UpdateChecker(APP_VERSION, UPDATE_SERVER_URL)
            update_info = checker.check_for_updates()
            
            # Restaurar estilo original del botón
            sender.setStyleSheet("")  # Volver al estilo por defecto
            sender.setText(original_text)
            sender.setEnabled(True)
            
            if update_info:
                # Mostrar diálogo de actualización disponible con mejor formato
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Question)
                msg.setWindowTitle("🆕 Actualización Disponible")
                
                # Estilos mejorados para el diálogo de actualización
                msg.setStyleSheet("""
                    QMessageBox {
                        background-color: white;
                        color: #2c3e50;
                        font-family: 'Segoe UI', Arial, sans-serif;
                        font-size: 14px;
                        min-width: 400px;
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
                        min-width: 100px;
                        margin: 5px;
                    }
                    QMessageBox QPushButton:hover {
                        background: qlineargradient(
                            x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #1a237e,
                            stop: 1 #0d1142
                        );
                    }
                    QMessageBox QPushButton[text="No"] {
                        background: qlineargradient(
                            x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #6c757d,
                            stop: 1 #495057
                        );
                    }
                    QMessageBox QPushButton[text="No"]:hover {
                        background: qlineargradient(
                            x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #495057,
                            stop: 1 #343a40
                        );
                    }
                """)
                
                msg.setText("<h2 style='color: #3153E4; margin-bottom: 15px;'>🚀 Nueva versión disponible!</h2>")
                msg.setInformativeText(f"<p style='color: #2c3e50; font-size: 14px; margin: 10px 0;'>"
                                     f"<strong>Versión actual:</strong> <span style='color: #6c757d;'>v{APP_VERSION}</span></p>"
                                     f"<p style='color: #2c3e50; font-size: 14px; margin: 10px 0;'>"
                                     f"<strong>Versión disponible:</strong> <span style='color: #00A26A; font-weight: bold;'>v{update_info['version']}</span></p>"
                                     f"<br><p style='color: #2c3e50; font-size: 14px;'>¿Desea <strong>descargar la actualización</strong> ahora?</p>")
                
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg.setDefaultButton(QMessageBox.Yes)
                
                reply = msg.exec()
                
                if reply == QMessageBox.Yes:
                    # Intentar proceso de actualización automática
                    try:
                        from src.utils.updater import AutoUpdater
                        updater = AutoUpdater(APP_VERSION, UPDATE_SERVER_URL, self.parent())
                        
                        # Crear un método personalizado para manejar fallos
                        def handle_download_failure():
                            self.show_manual_download_options(update_info)
                        
                        # Crear diálogo de actualización personalizado
                        from src.utils.updater import UpdateDialog
                        dialog = UpdateDialog(update_info, self)
                        
                        # Conectar señal de error para mostrar descarga manual
                        if hasattr(dialog, 'downloader') and dialog.downloader:
                            dialog.downloader.download_failed.connect(handle_download_failure)
                        
                        dialog.exec()
                        
                    except Exception as e:
                        # Si falla totalmente, mostrar descarga manual
                        self.show_manual_download_options(update_info)
                    
            else:
                # No hay actualizaciones - mensaje con mejor formato y colores
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("✅ Sin Actualizaciones")
                
                # Configurar estilos mejorados para mejor legibilidad
                msg.setStyleSheet("""
                    QMessageBox {
                        background-color: white;
                        color: #2c3e50;
                        font-family: 'Segoe UI', Arial, sans-serif;
                        font-size: 14px;
                    }
                    QMessageBox QLabel {
                        background-color: white;
                        color: #2c3e50;
                        padding: 15px;
                        font-size: 14px;
                        font-weight: normal;
                    }
                    QMessageBox QPushButton {
                        background: qlineargradient(
                            x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #00A26A,
                            stop: 1 #008854
                        );
                        color: white;
                        border: none;
                        border-radius: 5px;
                        padding: 10px 25px;
                        font-size: 14px;
                        font-weight: bold;
                        min-width: 80px;
                    }
                    QMessageBox QPushButton:hover {
                        background: qlineargradient(
                            x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #008854,
                            stop: 1 #006641
                        );
                    }
                """)
                
                msg.setText("<h2 style='color: #00A26A; margin-bottom: 15px;'>✅ Su aplicación está actualizada</h2>")
                msg.setInformativeText(f"<p style='color: #2c3e50; font-size: 14px; margin-bottom: 10px;'>"
                                     f"<strong>Versión actual:</strong> <span style='color: #00A26A; font-weight: bold;'>v{APP_VERSION}</span></p>"
                                     f"<p style='color: #27ae60; font-size: 14px;'>¡Está usando la versión más reciente!</p>")
                msg.exec()
                
        except Exception as e:
            # Restaurar botón en caso de error
            if 'sender' in locals():
                sender.setStyleSheet("")  # Volver al estilo por defecto
                sender.setText(original_text)
                sender.setEnabled(True)
            
            # Mensaje de error con mejor formato y colores
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("⚠️ Error de Conexión")
            
            # Estilos para el diálogo de error
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                    color: #2c3e50;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 14px;
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
                        stop: 0 #FF9040,
                        stop: 1 #E67E22
                    );
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px 25px;
                    font-size: 14px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #E67E22,
                        stop: 1 #D35400
                    );
                }
            """)
            
            msg.setText("<h2 style='color: #FF9040; margin-bottom: 15px;'>⚠️ No se pudo verificar actualizaciones</h2>")
            msg.setInformativeText(f"<p style='color: #2c3e50; font-size: 14px; margin: 10px 0;'>"
                                 f"<strong>Error:</strong> <span style='color: #e74c3c;'>{str(e)}</span></p>"
                                 f"<br><p style='color: #2c3e50; font-size: 14px;'>Verifique su conexión a Internet e intente nuevamente.</p>")
            msg.exec()
    
    def show_manual_download_options(self, update_info):
        """Mostrar opciones de descarga manual cuando falla la automática"""
        # Construir URLs de descarga
        version = update_info.get('version', 'latest')
        github_url = f"https://github.com/brunooviedo/AlertasQb/releases/tag/v{version}"
        download_url = update_info.get('download_url', github_url)
        
        # Crear diálogo personalizado para descarga manual
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("📥 Descarga Manual Disponible")
        
        # Estilos mejorados
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                min-width: 550px;
            }
            QMessageBox QLabel {
                background-color: white;
                color: #2c3e50;
                padding: 20px;
                font-size: 14px;
                line-height: 1.4;
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
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
                margin: 5px;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #1a237e,
                    stop: 1 #0d1142
                );
            }
            QMessageBox QPushButton[text="📋 Copiar"] {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #00A26A,
                    stop: 1 #008854
                );
            }
            QMessageBox QPushButton[text="📋 Copiar"]:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #008854,
                    stop: 1 #006641
                );
            }
        """)
        
        # Contenido del mensaje
        msg.setText(f"<h2 style='color: #3153E4; margin-bottom: 15px;'>📥 Descarga Manual - v{version}</h2>")
        
        msg.setInformativeText(f"""
            <p style='color: #e74c3c; font-size: 14px; font-weight: bold; margin-bottom: 15px;'>
                ❌ Error: La descarga automática falló
            </p>
            <p style='color: #2c3e50; font-size: 14px; margin-bottom: 20px;'>
                Para descargar la nueva versión <strong>v{version}</strong>, siga estos pasos:
            </p>
            <div style='background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #3153E4; margin: 10px 0;'>
                <p style='color: #2c3e50; font-size: 13px; margin: 5px 0;'>
                    <strong>📋 Opción 1: Copiar enlace</strong><br>
                    • Haga clic en "📋 Copiar" para copiar el enlace<br>
                    • Pegue el enlace en su navegador web<br>
                    • Descargue el archivo AlertasQB_vX.X.X.exe
                </p>
                <hr style='border: none; height: 1px; background: #dee2e6; margin: 10px 0;'>
                <p style='color: #2c3e50; font-size: 13px; margin: 5px 0;'>
                    <strong>🌐 Opción 2: Abrir directamente</strong><br>
                    • Haga clic en "🌐 Navegador" para abrir automáticamente<br>
                    • Su navegador se abrirá en la página de descarga<br>
                    • Descargue y ejecute el nuevo instalador
                </p>
            </div>
            <p style='color: #6c757d; font-size: 12px; margin-top: 15px;'>
                💡 <strong>Nota:</strong> Una vez descargado, cierre esta aplicación antes de instalar la nueva versión.
            </p>
        """)
        
        # Botones de acción
        copy_button = msg.addButton("📋 Copiar", QMessageBox.ActionRole)
        open_button = msg.addButton("🌐 Navegador", QMessageBox.ActionRole)
        close_button = msg.addButton("Cerrar", QMessageBox.RejectRole)
        
        # Ejecutar diálogo
        reply = msg.exec()
        
        # Manejar respuesta del usuario
        if msg.clickedButton() == copy_button:
            # Copiar enlace al portapapeles
            try:
                from PySide6.QtGui import QClipboard
                from PySide6.QtWidgets import QApplication
                clipboard = QApplication.clipboard()
                clipboard.setText(github_url)
                
                # Mensaje de confirmación
                confirm_msg = QMessageBox(self)
                confirm_msg.setIcon(QMessageBox.Information)
                confirm_msg.setWindowTitle("✅ Enlace Copiado")
                confirm_msg.setText("<h3 style='color: #00A26A;'>✅ Enlace copiado al portapapeles</h3>")
                confirm_msg.setInformativeText(f"<p style='color: #2c3e50;'>Puede pegarlo en su navegador para descargar la actualización.</p>")
                confirm_msg.setStyleSheet(msg.styleSheet())  # Usar los mismos estilos
                confirm_msg.exec()
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo copiar el enlace: {str(e)}")
        
        elif msg.clickedButton() == open_button:
            # Abrir enlace en el navegador
            try:
                import webbrowser
                webbrowser.open(github_url)
                
                # Mensaje de confirmación
                confirm_msg = QMessageBox(self)
                confirm_msg.setIcon(QMessageBox.Information)
                confirm_msg.setWindowTitle("🌐 Navegador Abierto")
                confirm_msg.setText("<h3 style='color: #3153E4;'>🌐 Página de descarga abierta</h3>")
                confirm_msg.setInformativeText(f"<p style='color: #2c3e50;'>Se abrió la página de descarga en su navegador predeterminado.</p>")
                confirm_msg.setStyleSheet(msg.styleSheet())  # Usar los mismos estilos
                confirm_msg.exec()
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo abrir el navegador: {str(e)}")
    
    @staticmethod
    def show_about(parent=None):
        """Método estático para mostrar el diálogo"""
        dialog = AboutDialog(parent)
        dialog.exec()
