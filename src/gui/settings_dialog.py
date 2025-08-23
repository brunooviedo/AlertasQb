"""
Diálogo de configuración de la aplicación
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                              QWidget, QLabel, QLineEdit, QSpinBox, QCheckBox,
                              QPushButton, QFormLayout, QGroupBox, QFileDialog,
                              QMessageBox, QComboBox, QTextEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import json
from pathlib import Path


class GeneralSettingsWidget(QWidget):
    """Widget para configuraciones generales"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Configuraciones de archivos
        files_group = QGroupBox("Archivos")
        files_layout = QFormLayout(files_group)
        
        # Directorio de datos
        data_dir_layout = QHBoxLayout()
        self.data_dir_edit = QLineEdit()
        self.data_dir_edit.setText("data")
        data_dir_button = QPushButton("Buscar")
        data_dir_button.clicked.connect(self.select_data_directory)
        data_dir_layout.addWidget(self.data_dir_edit)
        data_dir_layout.addWidget(data_dir_button)
        files_layout.addRow("Directorio de datos:", data_dir_layout)
        
        # Archivo Excel por defecto
        self.excel_file_edit = QLineEdit()
        self.excel_file_edit.setText("data/alertas_geotecnicas.xlsx")
        files_layout.addRow("Archivo Excel:", self.excel_file_edit)
        
        layout.addWidget(files_group)
        
        # Configuraciones de interfaz
        ui_group = QGroupBox("Interfaz")
        ui_layout = QFormLayout(ui_group)
        
        # Tema
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Claro", "Oscuro", "Sistema"])
        ui_layout.addRow("Tema:", self.theme_combo)
        
        # Idioma
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Español", "English"])
        ui_layout.addRow("Idioma:", self.language_combo)
        
        # Actualización automática
        self.auto_refresh_check = QCheckBox("Actualizar dashboard automáticamente")
        self.auto_refresh_check.setChecked(True)
        ui_layout.addRow("", self.auto_refresh_check)
        
        # Intervalo de actualización
        self.refresh_interval_spin = QSpinBox()
        self.refresh_interval_spin.setRange(5, 300)
        self.refresh_interval_spin.setValue(30)
        self.refresh_interval_spin.setSuffix(" segundos")
        ui_layout.addRow("Intervalo de actualización:", self.refresh_interval_spin)
        
        layout.addWidget(ui_group)
        
        layout.addStretch()
        
    def select_data_directory(self):
        """Selecciona el directorio de datos"""
        directory = QFileDialog.getExistingDirectory(self, "Seleccionar directorio de datos")
        if directory:
            self.data_dir_edit.setText(directory)


class AlertSettingsWidget(QWidget):
    """Widget para configuraciones de alertas"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Configuraciones de duplicados
        duplicates_group = QGroupBox("Detección de Duplicados")
        duplicates_layout = QFormLayout(duplicates_group)
        
        # Campos para detección
        self.duplicate_fields_edit = QTextEdit()
        self.duplicate_fields_edit.setMaximumHeight(80)
        self.duplicate_fields_edit.setText("FechaHora, TipoAlerta, Observaciones")
        duplicates_layout.addRow("Campos para comparar:", self.duplicate_fields_edit)
        
        # Tolerancia en tiempo
        self.time_tolerance_spin = QSpinBox()
        self.time_tolerance_spin.setRange(0, 60)
        self.time_tolerance_spin.setValue(0)
        self.time_tolerance_spin.setSuffix(" minutos")
        duplicates_layout.addRow("Tolerancia en tiempo:", self.time_tolerance_spin)
        
        layout.addWidget(duplicates_group)
        
        # Configuraciones de validación
        validation_group = QGroupBox("Validación")
        validation_layout = QFormLayout(validation_group)
        
        # Campos obligatorios
        self.required_fields_edit = QTextEdit()
        self.required_fields_edit.setMaximumHeight(80)
        self.required_fields_edit.setText("TipoAlerta, Observaciones")
        validation_layout.addRow("Campos obligatorios:", self.required_fields_edit)
        
        # Validar fechas
        self.validate_dates_check = QCheckBox("Validar formato de fechas")
        self.validate_dates_check.setChecked(True)
        validation_layout.addRow("", self.validate_dates_check)
        
        # Validar archivos de respaldo
        self.validate_backup_check = QCheckBox("Validar existencia de archivos de respaldo")
        validation_layout.addRow("", self.validate_backup_check)
        
        layout.addWidget(validation_group)
        
        # Configuraciones de notificaciones
        notifications_group = QGroupBox("Notificaciones")
        notifications_layout = QFormLayout(notifications_group)
        
        # Notificar alertas rojas
        self.notify_red_alerts_check = QCheckBox("Notificar alertas rojas")
        self.notify_red_alerts_check.setChecked(True)
        notifications_layout.addRow("", self.notify_red_alerts_check)
        
        # Email para notificaciones
        self.notification_email_edit = QLineEdit()
        self.notification_email_edit.setPlaceholderText("email@empresa.com")
        notifications_layout.addRow("Email de notificaciones:", self.notification_email_edit)
        
        layout.addWidget(notifications_group)
        
        layout.addStretch()


class DatabaseSettingsWidget(QWidget):
    """Widget para configuraciones de base de datos"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Configuración SQL Server
        sql_group = QGroupBox("SQL Server")
        sql_layout = QFormLayout(sql_group)
        
        self.sql_server_edit = QLineEdit()
        self.sql_server_edit.setPlaceholderText("localhost\\SQLEXPRESS")
        sql_layout.addRow("Servidor:", self.sql_server_edit)
        
        self.sql_database_edit = QLineEdit()
        self.sql_database_edit.setPlaceholderText("AlertasGeotecnicas")
        sql_layout.addRow("Base de datos:", self.sql_database_edit)
        
        self.sql_table_edit = QLineEdit()
        self.sql_table_edit.setText("alertas_geotecnicas")
        sql_layout.addRow("Tabla:", self.sql_table_edit)
        
        # Autenticación
        auth_group = QGroupBox("Autenticación")
        auth_layout = QFormLayout(auth_group)
        
        self.auth_type_combo = QComboBox()
        self.auth_type_combo.addItems(["Windows Authentication", "SQL Server Authentication"])
        self.auth_type_combo.currentTextChanged.connect(self.on_auth_type_changed)
        auth_layout.addRow("Tipo:", self.auth_type_combo)
        
        self.sql_username_edit = QLineEdit()
        self.sql_username_edit.setEnabled(False)
        auth_layout.addRow("Usuario:", self.sql_username_edit)
        
        self.sql_password_edit = QLineEdit()
        self.sql_password_edit.setEchoMode(QLineEdit.Password)
        self.sql_password_edit.setEnabled(False)
        auth_layout.addRow("Contraseña:", self.sql_password_edit)
        
        sql_layout.addRow("", auth_group)
        
        # Configuraciones de sincronización
        sync_group = QGroupBox("Sincronización")
        sync_layout = QFormLayout(sync_group)
        
        self.auto_sync_check = QCheckBox("Sincronización automática")
        sync_layout.addRow("", self.auto_sync_check)
        
        self.sync_interval_spin = QSpinBox()
        self.sync_interval_spin.setRange(1, 60)
        self.sync_interval_spin.setValue(15)
        self.sync_interval_spin.setSuffix(" minutos")
        sync_layout.addRow("Intervalo de sincronización:", self.sync_interval_spin)
        
        layout.addWidget(sql_group)
        layout.addWidget(sync_group)
        
        layout.addStretch()
        
    def on_auth_type_changed(self, auth_type):
        """Maneja el cambio de tipo de autenticación"""
        is_sql_auth = auth_type == "SQL Server Authentication"
        self.sql_username_edit.setEnabled(is_sql_auth)
        self.sql_password_edit.setEnabled(is_sql_auth)


class SettingsDialog(QDialog):
    """Diálogo principal de configuraciones"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_file = Path("config/settings.json")
        self.settings_file.parent.mkdir(exist_ok=True, parents=True)
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        self.setWindowTitle("Configuración")
        self.setModal(True)
        self.resize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Tabs
        self.general_widget = GeneralSettingsWidget()
        self.alert_widget = AlertSettingsWidget()
        self.database_widget = DatabaseSettingsWidget()
        
        self.tab_widget.addTab(self.general_widget, "General")
        self.tab_widget.addTab(self.alert_widget, "Alertas")
        self.tab_widget.addTab(self.database_widget, "Base de Datos")
        
        layout.addWidget(self.tab_widget)
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.test_button = QPushButton("Probar Configuración")
        self.test_button.clicked.connect(self.test_configuration)
        
        self.reset_button = QPushButton("Restablecer")
        self.reset_button.clicked.connect(self.reset_settings)
        
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_settings)
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.test_button)
        button_layout.addStretch()
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        # Estilos
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2E8B57;
            }
            
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 80px;
            }
            
            QPushButton:hover {
                background-color: #45a049;
            }
            
            QPushButton#reset_button {
                background-color: #ff9800;
            }
            
            QPushButton#cancel_button {
                background-color: #f44336;
            }
        """)
        
        self.reset_button.setObjectName("reset_button")
        self.cancel_button.setObjectName("cancel_button")
        
    def get_default_settings(self) -> dict:
        """Obtiene la configuración por defecto"""
        return {
            "general": {
                "data_directory": "data",
                "excel_file": "data/alertas_geotecnicas.xlsx",
                "theme": "Claro",
                "language": "Español",
                "auto_refresh": True,
                "refresh_interval": 30
            },
            "alerts": {
                "duplicate_fields": "FechaHora, TipoAlerta, Observaciones",
                "time_tolerance": 0,
                "required_fields": "TipoAlerta, Observaciones",
                "validate_dates": True,
                "validate_backup": False,
                "notify_red_alerts": True,
                "notification_email": ""
            },
            "database": {
                "sql_server": "",
                "sql_database": "",
                "sql_table": "alertas_geotecnicas",
                "auth_type": "Windows Authentication",
                "sql_username": "",
                "sql_password": "",
                "auto_sync": False,
                "sync_interval": 15
            }
        }
        
    def load_settings(self):
        """Carga la configuración desde archivo"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
            else:
                settings = self.get_default_settings()
                
            # Aplicar configuración a la interfaz
            self.apply_settings_to_ui(settings)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error cargando configuración: {str(e)}")
            self.apply_settings_to_ui(self.get_default_settings())
            
    def apply_settings_to_ui(self, settings: dict):
        """Aplica la configuración a la interfaz"""
        # General
        general = settings.get("general", {})
        self.general_widget.data_dir_edit.setText(general.get("data_directory", "data"))
        self.general_widget.excel_file_edit.setText(general.get("excel_file", "data/alertas_geotecnicas.xlsx"))
        
        theme_index = self.general_widget.theme_combo.findText(general.get("theme", "Claro"))
        if theme_index >= 0:
            self.general_widget.theme_combo.setCurrentIndex(theme_index)
            
        lang_index = self.general_widget.language_combo.findText(general.get("language", "Español"))
        if lang_index >= 0:
            self.general_widget.language_combo.setCurrentIndex(lang_index)
            
        self.general_widget.auto_refresh_check.setChecked(general.get("auto_refresh", True))
        self.general_widget.refresh_interval_spin.setValue(general.get("refresh_interval", 30))
        
        # Alertas
        alerts = settings.get("alerts", {})
        self.alert_widget.duplicate_fields_edit.setText(alerts.get("duplicate_fields", "FechaHora, TipoAlerta, Observaciones"))
        self.alert_widget.time_tolerance_spin.setValue(alerts.get("time_tolerance", 0))
        self.alert_widget.required_fields_edit.setText(alerts.get("required_fields", "TipoAlerta, Observaciones"))
        self.alert_widget.validate_dates_check.setChecked(alerts.get("validate_dates", True))
        self.alert_widget.validate_backup_check.setChecked(alerts.get("validate_backup", False))
        self.alert_widget.notify_red_alerts_check.setChecked(alerts.get("notify_red_alerts", True))
        self.alert_widget.notification_email_edit.setText(alerts.get("notification_email", ""))
        
        # Base de datos
        database = settings.get("database", {})
        self.database_widget.sql_server_edit.setText(database.get("sql_server", ""))
        self.database_widget.sql_database_edit.setText(database.get("sql_database", ""))
        self.database_widget.sql_table_edit.setText(database.get("sql_table", "alertas_geotecnicas"))
        
        auth_index = self.database_widget.auth_type_combo.findText(database.get("auth_type", "Windows Authentication"))
        if auth_index >= 0:
            self.database_widget.auth_type_combo.setCurrentIndex(auth_index)
            
        self.database_widget.sql_username_edit.setText(database.get("sql_username", ""))
        self.database_widget.sql_password_edit.setText(database.get("sql_password", ""))
        self.database_widget.auto_sync_check.setChecked(database.get("auto_sync", False))
        self.database_widget.sync_interval_spin.setValue(database.get("sync_interval", 15))
        
    def get_settings_from_ui(self) -> dict:
        """Obtiene la configuración de la interfaz"""
        return {
            "general": {
                "data_directory": self.general_widget.data_dir_edit.text(),
                "excel_file": self.general_widget.excel_file_edit.text(),
                "theme": self.general_widget.theme_combo.currentText(),
                "language": self.general_widget.language_combo.currentText(),
                "auto_refresh": self.general_widget.auto_refresh_check.isChecked(),
                "refresh_interval": self.general_widget.refresh_interval_spin.value()
            },
            "alerts": {
                "duplicate_fields": self.alert_widget.duplicate_fields_edit.toPlainText(),
                "time_tolerance": self.alert_widget.time_tolerance_spin.value(),
                "required_fields": self.alert_widget.required_fields_edit.toPlainText(),
                "validate_dates": self.alert_widget.validate_dates_check.isChecked(),
                "validate_backup": self.alert_widget.validate_backup_check.isChecked(),
                "notify_red_alerts": self.alert_widget.notify_red_alerts_check.isChecked(),
                "notification_email": self.alert_widget.notification_email_edit.text()
            },
            "database": {
                "sql_server": self.database_widget.sql_server_edit.text(),
                "sql_database": self.database_widget.sql_database_edit.text(),
                "sql_table": self.database_widget.sql_table_edit.text(),
                "auth_type": self.database_widget.auth_type_combo.currentText(),
                "sql_username": self.database_widget.sql_username_edit.text(),
                "sql_password": self.database_widget.sql_password_edit.text(),
                "auto_sync": self.database_widget.auto_sync_check.isChecked(),
                "sync_interval": self.database_widget.sync_interval_spin.value()
            }
        }
        
    def save_settings(self):
        """Guarda la configuración"""
        try:
            settings = self.get_settings_from_ui()
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
                
            QMessageBox.information(self, "Éxito", "Configuración guardada correctamente")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error guardando configuración: {str(e)}")
            
    def reset_settings(self):
        """Restablece la configuración por defecto"""
        reply = QMessageBox.question(
            self, 
            "Confirmar", 
            "¿Desea restablecer toda la configuración por defecto?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.apply_settings_to_ui(self.get_default_settings())
            
    def test_configuration(self):
        """Prueba la configuración actual"""
        settings = self.get_settings_from_ui()
        
        # Probar configuración de base de datos si está configurada
        db_config = settings["database"]
        if db_config["sql_server"] and db_config["sql_database"]:
            try:
                from src.data.sql_manager import SQLManager
                
                sql_manager = SQLManager(
                    server=db_config["sql_server"],
                    database=db_config["sql_database"],
                    username=db_config["sql_username"] if db_config["auth_type"] == "SQL Server Authentication" else None,
                    password=db_config["sql_password"] if db_config["auth_type"] == "SQL Server Authentication" else None,
                    table=db_config["sql_table"]
                )
                
                success, message = sql_manager.test_connection()
                
                if success:
                    QMessageBox.information(self, "Prueba Exitosa", "Conexión a base de datos exitosa")
                else:
                    QMessageBox.warning(self, "Error de Conexión", f"Error conectando a base de datos: {message}")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error probando configuración: {str(e)}")
        else:
            QMessageBox.information(self, "Configuración", "Configuración válida (base de datos no configurada)")
