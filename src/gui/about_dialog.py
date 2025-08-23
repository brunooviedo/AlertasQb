#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diálogo "Acerca de..." para el Sistema de Alertas Geotécnicas
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit
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
        update_button.setFixedSize(180, 35)
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
            from src.utils.updater import UpdateChecker
            from src.utils.version import UPDATE_SERVER_URL
            
            # Cambiar texto del botón mientras verifica
            sender = self.sender()
            original_text = sender.text()
            sender.setText("⏳ Verificando...")
            sender.setEnabled(False)
            
            # Procesar eventos para mostrar el cambio
            from PySide6.QtWidgets import QApplication
            QApplication.processEvents()
            
            # Verificar actualizaciones
            checker = UpdateChecker(APP_VERSION, UPDATE_SERVER_URL)
            update_info = checker.check_for_updates()
            
            # Restaurar botón
            sender.setText(original_text)
            sender.setEnabled(True)
            
            if update_info:
                # Mostrar diálogo de actualización disponible
                reply = QMessageBox.question(
                    self,
                    "Actualización Disponible",
                    f"🆕 Nueva versión disponible: v{update_info['version']}\n\n"
                    f"Versión actual: v{APP_VERSION}\n"
                    f"Versión disponible: v{update_info['version']}\n\n"
                    f"¿Desea descargar la actualización ahora?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )
                
                if reply == QMessageBox.Yes:
                    # Iniciar proceso de actualización
                    from src.utils.updater import AutoUpdater
                    updater = AutoUpdater(APP_VERSION, UPDATE_SERVER_URL, self.parent())
                    updater.start_update_process(update_info)
                    
            else:
                # No hay actualizaciones
                QMessageBox.information(
                    self,
                    "Sin Actualizaciones",
                    f"✅ Su aplicación está actualizada\n\nVersión actual: v{APP_VERSION}"
                )
                
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error de Conexión",
                f"⚠️ No se pudo verificar actualizaciones:\n{str(e)}\n\n"
                f"Verifique su conexión a Internet e intente nuevamente."
            )
            
            # Restaurar botón en caso de error
            if 'sender' in locals():
                sender.setText(original_text)
                sender.setEnabled(True)
    
    @staticmethod
    def show_about(parent=None):
        """Método estático para mostrar el diálogo"""
        dialog = AboutDialog(parent)
        dialog.exec()
