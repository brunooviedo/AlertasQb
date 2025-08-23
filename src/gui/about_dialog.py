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
        
        # Botón de cerrar
        button_layout = QHBoxLayout()
        close_button = QPushButton("Cerrar")
        close_button.setFixedSize(100, 35)
        close_button.setProperty("aboutClose", True)  # Usar propiedad CSS
        close_button.clicked.connect(self.accept)
        
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
    @staticmethod
    def show_about(parent=None):
        """Método estático para mostrar el diálogo"""
        dialog = AboutDialog(parent)
        dialog.exec()
