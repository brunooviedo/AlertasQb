"""Formulario para crear y editar alertas geotécnicas"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QTextEdit, QPushButton,
    QDateTimeEdit, QFileDialog, QMessageBox, QLabel,
    QFrame, QGroupBox, QSizePolicy
)
from PySide6.QtCore import Qt, QDateTime, Signal
from datetime import datetime

from src.data.excel_manager import ExcelManager
from src.auth.login_manager import User
from src.gui.styles.form_styles import FormStyles


class AlertForm(QWidget):
    """Formulario para registrar alertas geotécnicas"""

    alert_saved = Signal(dict)

    def __init__(self) -> None:
        super().__init__()
        self.current_user: User | None = None
        self.excel_manager = ExcelManager()
        self.setup_ui()
        self.setStyleSheet(FormStyles.get_complete_form_styles())

    # ---------------------------- UI SETUP ---------------------------- #
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Título
        title = QLabel("Registro de Nueva Alerta Geotécnica")
        title.setAlignment(Qt.AlignCenter)
        title.setProperty("titleLabel", True)
        title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(title)

        # Contenedor principal
        form_frame = QFrame()
        form_frame.setFrameStyle(QFrame.StyledPanel)
        form_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(12, 8, 12, 8)
        form_layout.setSpacing(8)

        # Grupo 1: Información básica
        basic_group = QGroupBox("Información Básica")
        basic_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        basic_layout = QFormLayout(basic_group)
        basic_layout.setContentsMargins(8, 6, 8, 6)
        basic_layout.setSpacing(6)
        basic_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.setDateTime(QDateTime.currentDateTime())
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self.datetime_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        basic_layout.addRow("Fecha y Hora:", self.datetime_edit)

        self.alert_type_combo = QComboBox()
        self.alert_type_combo.addItems(["Amarilla", "Naranja", "Roja"])
        self.alert_type_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        basic_layout.addRow("Tipo de Alerta:", self.alert_type_combo)

        self.condition_combo = QComboBox()
        self.condition_combo.addItems([
            "Transgresiva", 
            "Progresiva", 
            "Crítica", 
            "Regresiva", 
            "Transgresiva-Progresiva", 
            "Progresiva-Crítica"
        ])
        self.condition_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        basic_layout.addRow("Condición:", self.condition_combo)

        # Campo Ubicación (con validación)
        self.location_edit = QLineEdit()
        self.location_edit.setPlaceholderText("Ej: B4075 F1 Inferior, Sector Norte...")
        self.location_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.location_edit.textChanged.connect(self.validate_location)
        basic_layout.addRow("Ubicación:", self.location_edit)

        # Campo Velocidad mm/día (con validación numérica)
        self.velocity_edit = QLineEdit()
        self.velocity_edit.setPlaceholderText("Ej: 15.5 (solo números)")
        self.velocity_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.velocity_edit.textChanged.connect(self.validate_velocity)
        basic_layout.addRow("Velocidad (mm/día):", self.velocity_edit)

        form_layout.addWidget(basic_group)

        # Grupo 2: Detalles del evento
        details_group = QGroupBox("Detalles del Evento")
        details_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        details_layout = QFormLayout(details_group)
        details_layout.setContentsMargins(8, 6, 8, 6)
        details_layout.setSpacing(6)
        details_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        backup_container = QHBoxLayout()
        self.backup_path = QLineEdit()
        self.backup_path.setPlaceholderText("Seleccione el archivo PowerPoint...")
        self.backup_path.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.backup_button = QPushButton("Buscar...")
        self.backup_button.setFixedWidth(95)
        self.backup_button.clicked.connect(self.select_backup_file)
        backup_container.addWidget(self.backup_path)
        backup_container.addWidget(self.backup_button)
        details_layout.addRow("Respaldo (PowerPoint):", backup_container)

        self.collapse_combo = QComboBox()
        self.collapse_combo.addItems(["No", "Sí"])
        self.collapse_combo.currentTextChanged.connect(self.on_collapse_changed)
        self.collapse_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        details_layout.addRow("Colapso:", self.collapse_combo)

        self.collapse_datetime = QDateTimeEdit()
        self.collapse_datetime.setDateTime(QDateTime.currentDateTime())
        self.collapse_datetime.setCalendarPopup(True)
        self.collapse_datetime.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self.collapse_datetime.setEnabled(False)
        self.collapse_datetime.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        details_layout.addRow("Fecha/Hora Colapso:", self.collapse_datetime)

        self.evacuation_combo = QComboBox()
        self.evacuation_combo.addItems(["No", "Sí"])
        self.evacuation_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        details_layout.addRow("Evacuación:", self.evacuation_combo)

        form_layout.addWidget(details_group)

        # Grupo 3: Análisis y observaciones
        analysis_group = QGroupBox("Análisis y Observaciones")
        analysis_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        analysis_layout = QFormLayout(analysis_group)
        analysis_layout.setContentsMargins(8, 6, 8, 6)
        analysis_layout.setSpacing(6)
        analysis_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        self.chronology_text = QTextEdit()
        self.chronology_text.setMinimumHeight(60)
        self.chronology_text.setMaximumHeight(100)
        self.chronology_text.setPlaceholderText("Describa la cronología y análisis del evento...")
        self.chronology_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        analysis_layout.addRow("Cronología/Análisis:", self.chronology_text)

        self.observations_text = QTextEdit()
        self.observations_text.setMinimumHeight(60)
        self.observations_text.setMaximumHeight(100)
        self.observations_text.setPlaceholderText("Ingrese observaciones adicionales...")
        self.observations_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        analysis_layout.addRow("Observaciones:", self.observations_text)

        form_layout.addWidget(analysis_group)

        layout.addWidget(form_frame)

        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 8, 0, 0)
        buttons_layout.setSpacing(8)
        buttons_layout.addStretch()

        self.clear_button = QPushButton("Limpiar")
        self.clear_button.clicked.connect(self.clear_form)
        self.clear_button.setProperty("clearButton", True)

        self.save_button = QPushButton("Guardar Alerta")
        self.save_button.clicked.connect(self.save_alert)
        self.save_button.setProperty("saveButton", True)

        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.save_button)
        layout.addLayout(buttons_layout)

    # ---------------------------- LOGIC ---------------------------- #
    def set_current_user(self, user: User):
        """Establece el usuario actual y configura permisos"""
        self.current_user = user
        
        # Configurar permisos según el rol del usuario
        from src.auth.login_manager import AuthManager
        auth_manager = AuthManager()
        can_write = auth_manager.has_permission(user, "write")
        
        # Si el usuario no tiene permisos de escritura, deshabilitar campos
        if not can_write:
            self.disable_form_for_readonly()
        
    def disable_form_for_readonly(self):
        """Deshabilita el formulario para usuarios de solo lectura"""
        # Deshabilitar todos los campos de entrada
        self.datetime_edit.setEnabled(False)
        self.alert_type_combo.setEnabled(False)
        self.condition_combo.setEnabled(False)
        self.backup_path.setEnabled(False)
        self.backup_button.setEnabled(False)
        self.collapse_combo.setEnabled(False)
        self.collapse_datetime.setEnabled(False)
        self.evacuation_combo.setEnabled(False)
        self.chronology_text.setEnabled(False)
        self.observations_text.setEnabled(False)
        
        # Deshabilitar botones
        self.clear_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.save_button.setText("🔒 Solo Lectura")
        
        # Agregar mensaje informativo
        readonly_label = getattr(self, 'readonly_label', None)
        if not readonly_label:
            from PySide6.QtWidgets import QLabel
            from PySide6.QtCore import Qt
            readonly_label = QLabel("⚠️ Usuario en modo solo lectura - No se pueden crear nuevas alertas")
            readonly_label.setAlignment(Qt.AlignCenter)
            readonly_label.setStyleSheet("""
                QLabel {
                    background-color: #ffc107;
                    color: #856404;
                    padding: 10px;
                    border-radius: 5px;
                    font-weight: bold;
                    margin: 10px 0;
                }
            """)
            # Insertar al inicio del layout
            layout = self.layout()
            layout.insertWidget(0, readonly_label)
            self.readonly_label = readonly_label

    def on_collapse_changed(self, value: str):
        self.collapse_datetime.setEnabled(value == "Sí")

    def select_backup_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo PowerPoint",
            "",
            "PowerPoint Files (*.ppt *.pptx);;All Files (*)"
        )
        if file_path:
            self.backup_path.setText(file_path)

    def validate_form(self) -> bool:
        """Valida todos los campos del formulario con validaciones robustas"""
        if not self.current_user:
            QMessageBox.warning(self, "Error", "No hay usuario autenticado")
            return False
        
        # Validar observaciones (obligatorio)
        if not self.observations_text.toPlainText().strip():
            QMessageBox.warning(self, "Error", "Las observaciones son obligatorias")
            return False
        
        # Validar ubicación (obligatorio)
        if not self.location_edit.text().strip():
            QMessageBox.warning(self, "Error", "La ubicación es obligatoria")
            return False
        
        # Validar velocidad (obligatorio y formato numérico)
        velocity_text = self.velocity_edit.text().strip()
        if not velocity_text:
            QMessageBox.warning(self, "Error", "La velocidad (mm/día) es obligatoria")
            return False
        
        try:
            velocity_value = float(velocity_text.replace(',', '.'))  # Permitir coma como decimal
            if velocity_value < 0:
                QMessageBox.warning(self, "Error", "La velocidad no puede ser negativa")
                return False
        except ValueError:
            QMessageBox.warning(self, "Error", 
                              "La velocidad debe ser un número válido (ej: 15.5, 20,3)")
            return False
        
        # Validar fecha (no puede ser futura más allá del límite razonable)
        current_datetime = QDateTime.currentDateTime()
        selected_datetime = self.datetime_edit.dateTime()
        
        if selected_datetime > current_datetime.addDays(1):  # Permitir hasta 1 día en el futuro
            QMessageBox.warning(self, "Error", 
                              "La fecha no puede estar más de 1 día en el futuro")
            return False
        
        # Validar fecha de colapso si aplica
        if self.collapse_combo.currentText() == "Sí":
            collapse_datetime = self.collapse_datetime.dateTime()
            if collapse_datetime < selected_datetime:
                QMessageBox.warning(self, "Error", 
                                  "La fecha de colapso no puede ser anterior a la fecha de la alerta")
                return False
        
        # Validar respaldo (opcional pero debe ser un archivo válido si se proporciona)
        backup_path = self.backup_path.text().strip()
        if backup_path:
            from pathlib import Path
            if not Path(backup_path).exists():
                reply = QMessageBox.question(self, "Advertencia", 
                                           f"El archivo de respaldo no existe:\n{backup_path}\n\n"
                                           "¿Desea continuar sin el archivo de respaldo?",
                                           QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    return False
        
        return True

    def get_form_data(self) -> dict:
        """Obtiene los datos del formulario con formato garantizado"""
        # Obtener fecha y hora en formato correcto (YYYY-MM-DD HH:MM:SS)
        selected_datetime = self.datetime_edit.dateTime()
        fecha_hora = selected_datetime.toString("yyyy-MM-dd hh:mm:ss")
        
        # Fecha de colapso si aplica
        collapse_datetime = None
        if self.collapse_combo.currentText() == "Sí":
            collapse_dt = self.collapse_datetime.dateTime()
            collapse_datetime = collapse_dt.toString("yyyy-MM-dd hh:mm:ss")
        
        # Normalizar velocidad (reemplazar coma por punto)
        velocity_text = self.velocity_edit.text().strip().replace(',', '.')
        
        # Normalizar condición (primera letra mayúscula)
        condition = self.condition_combo.currentText()
        condition = condition.capitalize() if condition else ""
        
        return {
            "FechaHora": fecha_hora,  # Formato estándar: YYYY-MM-DD HH:MM:SS
            "TipoAlerta": self.alert_type_combo.currentText(),
            "Condicion": condition,
            "Ubicacion": self.location_edit.text().strip(),
            "VelocidadMmDia": velocity_text,
            "Respaldo": self.backup_path.text().strip(),
            "Colapso": self.collapse_combo.currentText(),
            "FechaHoraColapso": collapse_datetime,
            "Evacuacion": self.evacuation_combo.currentText(),
            "CronologiaAnalisis": self.chronology_text.toPlainText().strip(),
            "Observaciones": self.observations_text.toPlainText().strip(),
            "Usuario": self.current_user.username if self.current_user else "Desconocido",
            "FechaRegistro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formato estándar
        }

    def save_alert(self):
        if not self.validate_form():
            return
        try:
            alert_data = self.get_form_data()
            success = self.excel_manager.save_alert(alert_data)
            if success:
                QMessageBox.information(self, "Éxito", "Alerta guardada correctamente")
                self.alert_saved.emit(alert_data)
                self.clear_form()
            else:
                QMessageBox.critical(self, "Error", "No se pudo guardar la alerta")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar: {e}")

    def clear_form(self):
        self.datetime_edit.setDateTime(QDateTime.currentDateTime())
        self.alert_type_combo.setCurrentIndex(0)
        self.condition_combo.setCurrentIndex(0)
        self.location_edit.clear()
        self.velocity_edit.clear()
        self.backup_path.clear()
        self.collapse_combo.setCurrentIndex(0)
        self.collapse_datetime.setDateTime(QDateTime.currentDateTime())
        self.evacuation_combo.setCurrentIndex(0)
        self.chronology_text.clear()
        self.observations_text.clear()

    def set_read_only(self, read_only=True):
        """Configura el formulario en modo solo lectura"""
        # Deshabilitar todos los campos de entrada
        self.datetime_edit.setEnabled(not read_only)
        self.alert_type_combo.setEnabled(not read_only)
        self.condition_combo.setEnabled(not read_only)
        self.location_edit.setEnabled(not read_only)
        self.velocity_edit.setEnabled(not read_only)
        self.backup_path.setEnabled(not read_only)
        self.collapse_combo.setEnabled(not read_only)
        self.collapse_datetime.setEnabled(not read_only)
        self.evacuation_combo.setEnabled(not read_only)
        self.chronology_text.setEnabled(not read_only)
        self.observations_text.setEnabled(not read_only)
        
        # Deshabilitar botones de acción
        self.save_button.setEnabled(not read_only)
        self.clear_button.setEnabled(not read_only)
        
        if read_only:
            self.save_button.setText("🔒 Solo Lectura")
            
            # Agregar mensaje informativo si no existe
            if not hasattr(self, 'readonly_label'):
                from PySide6.QtWidgets import QLabel
                from PySide6.QtCore import Qt
                readonly_label = QLabel("⚠️ Usuario en modo solo lectura - No se pueden crear nuevas alertas")
                readonly_label.setAlignment(Qt.AlignCenter)
                readonly_label.setStyleSheet("""
                    QLabel {
                        background-color: #ffc107;
                        color: #856404;
                        padding: 10px;
                        border-radius: 5px;
                        font-weight: bold;
                        margin: 10px 0;
                    }
                """)
                # Insertar al inicio del layout
                layout = self.layout()
                layout.insertWidget(0, readonly_label)
                self.readonly_label = readonly_label
        else:
            self.save_button.setText("Guardar Alerta")
            # Remover mensaje informativo si existe
            if hasattr(self, 'readonly_label'):
                self.readonly_label.setParent(None)
    
    # ---------------------------- VALIDACIONES EN TIEMPO REAL ---------------------------- #
    
    def validate_velocity(self, text: str):
        """Valida el campo de velocidad en tiempo real"""
        # Permitir vacío, números, punto y coma
        if not text:
            self.velocity_edit.setStyleSheet("")
            return
        
        # Reemplazar coma por punto para validación
        normalized_text = text.replace(',', '.')
        
        try:
            value = float(normalized_text)
            if value < 0:
                # Valor negativo - mostrar como error
                self.velocity_edit.setStyleSheet("""
                    QLineEdit {
                        border: 2px solid #e74c3c;
                        background-color: #fdf2f2;
                    }
                """)
            else:
                # Valor válido - mostrar como correcto
                self.velocity_edit.setStyleSheet("""
                    QLineEdit {
                        border: 2px solid #27ae60;
                        background-color: #f8fff8;
                    }
                """)
        except ValueError:
            # Formato inválido - mostrar como error
            self.velocity_edit.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #e74c3c;
                    background-color: #fdf2f2;
                }
            """)
    
    def validate_location(self, text: str):
        """Valida el campo de ubicación en tiempo real"""
        if not text.strip():
            self.location_edit.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #f39c12;
                    background-color: #fef9e7;
                }
            """)
        else:
            self.location_edit.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #27ae60;
                    background-color: #f8fff8;
                }
            """)
