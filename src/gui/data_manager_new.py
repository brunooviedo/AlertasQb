"""
Widget simplificado para gestión de datos (importar/exportar Excel, SQL Server)
Solo operaciones, sin visualización de datos
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QTextEdit, QPushButton,
    QFileDialog, QMessageBox, QLabel,
    QFrame, QGroupBox, QSizePolicy, QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
import pandas as pd
from pathlib import Path

from src.data.excel_manager import ExcelManager
from src.data.sql_manager import SQLManager


class ImportExportThread(QThread):
    """Thread para operaciones de importación/exportación"""
    
    progress = Signal(int)
    finished = Signal(bool, str)
    
    def __init__(self, operation: str, **kwargs):
        super().__init__()
        self.operation = operation
        self.kwargs = kwargs
        
    def run(self):
        try:
            if self.operation == "import_excel":
                excel_manager = ExcelManager()
                success, message = excel_manager.import_excel(self.kwargs['file_path'])
                self.finished.emit(success, message)
                
            elif self.operation == "export_excel":
                excel_manager = ExcelManager()
                success = excel_manager.export_excel(self.kwargs['file_path'])
                message = "Exportación exitosa" if success else "Error en exportación"
                self.finished.emit(success, message)
                
            elif self.operation == "export_sql":
                sql_manager = SQLManager(**self.kwargs['connection'])
                success, message = sql_manager.export_to_sql()
                self.finished.emit(success, message)
                
            elif self.operation == "import_sql":
                sql_manager = SQLManager(**self.kwargs['connection'])
                success, message = sql_manager.import_from_sql()
                self.finished.emit(success, message)
                
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")


class SQLConfigWidget(QWidget):
    """Widget para configuración de conexión SQL"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz SQL"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 12)
        layout.setSpacing(12)
        
        # Grupo de configuración
        config_group = QGroupBox("Configuración SQL Server")
        config_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        config_layout = QFormLayout(config_group)
        config_layout.setContentsMargins(12, 10, 12, 12)
        config_layout.setSpacing(12)
        config_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("Servidor SQL (ej: localhost)")
        self.server_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        config_layout.addRow("Servidor:", self.server_input)
        
        self.database_input = QLineEdit()
        self.database_input.setPlaceholderText("Nombre de base de datos")
        self.database_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        config_layout.addRow("Base de Datos:", self.database_input)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario (opcional para Windows Auth)")
        self.username_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        config_layout.addRow("Usuario:", self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Contraseña (opcional para Windows Auth)")
        self.password_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        config_layout.addRow("Contraseña:", self.password_input)
        
        layout.addWidget(config_group)
        
        # Botones SQL
        sql_buttons_layout = QHBoxLayout()
        sql_buttons_layout.setSpacing(12)
        
        self.test_connection_button = QPushButton("Probar Conexión")
        self.export_sql_button = QPushButton("Exportar a SQL")
        self.import_sql_button = QPushButton("Importar desde SQL")
        
        sql_buttons_layout.addWidget(self.test_connection_button)
        sql_buttons_layout.addWidget(self.export_sql_button)
        sql_buttons_layout.addWidget(self.import_sql_button)
        sql_buttons_layout.addStretch()
        
        layout.addLayout(sql_buttons_layout)
        
        # Log
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(120)
        self.log_text.setPlaceholderText("Log de operaciones SQL...")
        layout.addWidget(self.log_text)
        
    def get_connection_config(self) -> dict:
        """Obtiene la configuración de conexión"""
        return {
            'server': self.server_input.text().strip(),
            'database': self.database_input.text().strip(),
            'username': self.username_input.text().strip() or None,
            'password': self.password_input.text().strip() or None
        }
        
    def add_log(self, message: str):
        """Añade mensaje al log"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")


class DataManagerWidget(QWidget):
    """Widget simplificado para gestión de datos - solo operaciones"""
    
    def __init__(self):
        super().__init__()
        self.excel_manager = ExcelManager()
        self.current_thread = None
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        """Configura la interfaz principal"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)
        
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Título
        title = QLabel("Gestión de Datos")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(title)
        
        # Contenedor principal
        main_frame = QFrame()
        main_frame.setFrameStyle(QFrame.StyledPanel)
        main_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout = QVBoxLayout(main_frame)
        main_layout.setContentsMargins(24, 18, 24, 20)
        main_layout.setSpacing(18)
        
        # Grupo Excel
        excel_group = QGroupBox("Operaciones Excel")
        excel_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        excel_layout = QVBoxLayout(excel_group)
        excel_layout.setContentsMargins(12, 10, 12, 12)
        excel_layout.setSpacing(12)
        
        # Descripción
        excel_desc = QLabel("Importe, exporte y gestione plantillas de archivos Excel con alertas geotécnicas.")
        excel_desc.setWordWrap(True)
        excel_layout.addWidget(excel_desc)
        
        # Botones Excel
        excel_buttons_layout = QHBoxLayout()
        excel_buttons_layout.setSpacing(12)
        
        self.import_excel_button = QPushButton("Importar Excel")
        self.import_excel_button.clicked.connect(self.import_excel)
        
        self.export_excel_button = QPushButton("Exportar Excel")
        self.export_excel_button.clicked.connect(self.export_excel)
        
        self.create_template_button = QPushButton("Crear Plantilla")
        self.create_template_button.clicked.connect(self.create_template)
        
        excel_buttons_layout.addWidget(self.import_excel_button)
        excel_buttons_layout.addWidget(self.export_excel_button)
        excel_buttons_layout.addWidget(self.create_template_button)
        excel_buttons_layout.addStretch()
        
        excel_layout.addLayout(excel_buttons_layout)
        main_layout.addWidget(excel_group)
        
        # Grupo SQL
        sql_group = QGroupBox("Operaciones SQL Server")
        sql_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sql_layout = QVBoxLayout(sql_group)
        sql_layout.setContentsMargins(12, 10, 12, 12)
        sql_layout.setSpacing(12)
        
        # Descripción
        sql_desc = QLabel("Configure la conexión a SQL Server para sincronizar datos de alertas.")
        sql_desc.setWordWrap(True)
        sql_layout.addWidget(sql_desc)
        
        # Widget SQL
        self.sql_config = SQLConfigWidget()
        self.sql_config.test_connection_button.clicked.connect(self.test_sql_connection)
        self.sql_config.export_sql_button.clicked.connect(self.export_to_sql)
        self.sql_config.import_sql_button.clicked.connect(self.import_from_sql)
        sql_layout.addWidget(self.sql_config)
        
        sql_group.setLayout(sql_layout)
        main_layout.addWidget(sql_group)
        
        layout.addWidget(main_frame)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

    # ---------------------------- STYLES ---------------------------- #
    def apply_styles(self):
        self.setStyleSheet(
            """
            QGroupBox { font-weight: bold; border: 1px solid #c9c9c9; border-radius: 8px; margin-top: 14px; padding-top: 8px; background: #fcfcfc; color: #000000; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; color: #2E7D4F; }
            QLineEdit, QComboBox, QTextEdit { border: 1px solid #d2d2d2; border-radius: 6px; padding: 6px 8px; font-size: 13px; background: #ffffff; color: #000000; }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus { border-color: #4CAF50; outline: none; }
            QPushButton { background-color: #4CAF50; color: #ffffff; border: none; padding: 8px 18px; border-radius: 5px; font-size: 13px; font-weight: bold; min-width: 110px; }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:pressed { background-color: #3d8b40; }
            QPushButton:disabled { background-color: #cccccc; color: #666666; }
            QLabel { font-size: 13px; color: #000000; }
            QTextEdit { line-height: 1.25; }
            QProgressBar { border: 1px solid #d2d2d2; border-radius: 6px; text-align: center; color: #000000; }
            QProgressBar::chunk { background-color: #4CAF50; border-radius: 5px; }
            """
        )

    # ---------------------------- EXCEL OPERATIONS ---------------------------- #
    def import_excel(self):
        """Importa datos desde un archivo Excel"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Seleccionar archivo Excel", 
            "", 
            "Excel Files (*.xlsx *.xls);;All Files (*)"
        )
        
        if file_path:
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminado
            
            self.current_thread = ImportExportThread("import_excel", file_path=file_path)
            self.current_thread.finished.connect(self.on_operation_finished)
            self.current_thread.start()
            
    def export_excel(self):
        """Exporta datos a un archivo Excel"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar archivo Excel",
            f"alertas_geotecnicas_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            "Excel Files (*.xlsx);;All Files (*)"
        )
        
        if file_path:
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)
            
            self.current_thread = ImportExportThread("export_excel", file_path=file_path)
            self.current_thread.finished.connect(self.on_operation_finished)
            self.current_thread.start()
            
    def create_template(self):
        """Crea una plantilla Excel vacía"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar plantilla Excel",
            "plantilla_alertas.xlsx",
            "Excel Files (*.xlsx);;All Files (*)"
        )
        
        if file_path:
            try:
                # Crear DataFrame vacío con las columnas necesarias
                columns = [
                    "FechaHora", "TipoAlerta", "Condicion", "Respaldo", 
                    "Colapso", "FechaHoraColapso", "Evacuacion", 
                    "CronologiaAnalisis", "Observaciones", "Usuario", "FechaRegistro"
                ]
                
                df = pd.DataFrame(columns=columns)
                
                # Agregar algunas filas de ejemplo
                ejemplo = {
                    "FechaHora": "01/01/2024 10:30:00",
                    "TipoAlerta": "Amarilla",
                    "Condicion": "transgresiva",
                    "Respaldo": "C:\\documentos\\presentacion.pptx",
                    "Colapso": "No",
                    "FechaHoraColapso": "",
                    "Evacuacion": "No",
                    "CronologiaAnalisis": "Descripción del análisis...",
                    "Observaciones": "Observaciones detalladas...",
                    "Usuario": "usuario_ejemplo",
                    "FechaRegistro": "01/01/2024 10:35:00"
                }
                
                df = pd.concat([df, pd.DataFrame([ejemplo])], ignore_index=True)
                
                # Guardar
                temp_manager = ExcelManager(file_path)
                temp_manager._save_formatted_excel_to_path(df, file_path)
                
                QMessageBox.information(self, "Éxito", "Plantilla creada correctamente")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error creando plantilla: {e}")

    # ---------------------------- SQL OPERATIONS ---------------------------- #
    def test_sql_connection(self):
        """Prueba la conexión a SQL Server"""
        try:
            config = self.sql_config.get_connection_config()
            
            if not config['server'] or not config['database']:
                QMessageBox.warning(self, "Error", "Servidor y base de datos son obligatorios")
                return
                
            sql_manager = SQLManager(**config)
            success, message = sql_manager.test_connection()
            
            if success:
                QMessageBox.information(self, "Éxito", "Conexión exitosa")
                self.sql_config.add_log("Conexión exitosa")
            else:
                QMessageBox.warning(self, "Error", f"Error de conexión: {message}")
                self.sql_config.add_log(f"Error: {message}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {e}")
            self.sql_config.add_log(f"Error: {e}")
            
    def export_to_sql(self):
        """Exporta datos a SQL Server"""
        config = self.sql_config.get_connection_config()
        
        if not config['server'] or not config['database']:
            QMessageBox.warning(self, "Error", "Configuración SQL incompleta")
            return
            
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        self.current_thread = ImportExportThread("export_sql", connection=config)
        self.current_thread.finished.connect(self.on_sql_operation_finished)
        self.current_thread.start()
        
    def import_from_sql(self):
        """Importa datos desde SQL Server"""
        config = self.sql_config.get_connection_config()
        
        if not config['server'] or not config['database']:
            QMessageBox.warning(self, "Error", "Configuración SQL incompleta")
            return
            
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        self.current_thread = ImportExportThread("import_sql", connection=config)
        self.current_thread.finished.connect(self.on_sql_operation_finished)
        self.current_thread.start()

    # ---------------------------- EVENT HANDLERS ---------------------------- #
    def on_operation_finished(self, success: bool, message: str):
        """Maneja el fin de una operación Excel"""
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "Éxito", message)
        else:
            QMessageBox.critical(self, "Error", message)
            
    def on_sql_operation_finished(self, success: bool, message: str):
        """Maneja el fin de una operación SQL"""
        self.progress_bar.setVisible(False)
        self.sql_config.add_log(message)
        
        if success:
            QMessageBox.information(self, "Éxito", message)
        else:
            QMessageBox.critical(self, "Error", message)
