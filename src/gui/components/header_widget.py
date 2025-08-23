"""
Widget de cabecera para la ventana principal
Contiene el título, información del usuario y fecha/hora
"""

from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from datetime import datetime


class HeaderWidget(QFrame):
    """Widget de cabecera con título, información de usuario y fecha/hora"""
    
    def __init__(self, parent=None):
        """
        Inicializa el widget de cabecera
        
        Args:
            parent: Widget padre
        """
        super().__init__(parent)
        self.user_info_label = None
        self.datetime_label = None
        self.timer = None
        self.setup_ui()
        self.setup_timer()
    
    def setup_ui(self):
        """Configura la interfaz del header"""
        self.setFrameStyle(QFrame.StyledPanel)
        self.setFixedHeight(80)  # Altura fija para evitar cambios
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # Layout principal del header
        header_layout = QHBoxLayout(self)
        header_layout.setContentsMargins(20, 10, 20, 10)
        header_layout.setSpacing(15)
        
        # Crear componentes
        title_widget = self._create_title_widget()
        user_info_widget = self._create_user_info_widget()
        
        # Agregar componentes al layout
        header_layout.addWidget(title_widget)
        header_layout.addStretch()
        header_layout.addLayout(user_info_widget)
    
    def _create_title_widget(self) -> QLabel:
        """Crea el widget del título/logo"""
        title_label = QLabel("Sistema de Alertas Geotécnicas")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #007bff; font-family: 'Segoe UI';")
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, 
                                 QSizePolicy.Policy.Preferred)
        return title_label
    
    def _create_user_info_widget(self) -> QVBoxLayout:
        """Crea el widget de información del usuario"""
        user_container = QVBoxLayout()
        user_container.setSpacing(3)
        
        # Información del usuario
        self.user_info_label = QLabel("Usuario: No autenticado")
        self.user_info_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.user_info_label.setStyleSheet("""
            color: #495057; 
            font-size: 14px; 
            font-weight: 600;
            font-family: 'Segoe UI';
        """)
        self.user_info_label.setSizePolicy(QSizePolicy.Policy.Preferred, 
                                          QSizePolicy.Policy.Preferred)
        
        # Fecha y hora actual
        self.datetime_label = QLabel()
        self.datetime_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.datetime_label.setStyleSheet("""
            color: #6c757d; 
            font-size: 12px;
            font-family: 'Segoe UI';
        """)
        self.datetime_label.setSizePolicy(QSizePolicy.Policy.Preferred, 
                                         QSizePolicy.Policy.Preferred)
        
        user_container.addWidget(self.user_info_label)
        user_container.addWidget(self.datetime_label)
        
        return user_container
    
    def setup_timer(self):
        """Configura el timer para actualizar la fecha/hora"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)  # Actualizar cada segundo
        
        # Actualizar inmediatamente
        self.update_datetime()
    
    def update_datetime(self):
        """Actualiza la fecha y hora mostrada"""
        if self.datetime_label:
            now = datetime.now()
            fecha_str = now.strftime("%d/%m/%Y %H:%M:%S")
            self.datetime_label.setText(f"Fecha: {fecha_str}")
    
    def set_user_info(self, user_name: str, role: str = ""):
        """
        Actualiza la información del usuario en el header
        
        Args:
            user_name: Nombre del usuario
            role: Rol del usuario (opcional)
        """
        if self.user_info_label:
            if role:
                text = f"Usuario: {user_name} ({role})"
            else:
                text = f"Usuario: {user_name}"
            self.user_info_label.setText(text)
    
    def set_title(self, title: str):
        """
        Cambia el título del header
        
        Args:
            title: Nuevo título
        """
        # Buscar el label del título en el layout
        layout = self.layout()
        if layout and layout.count() > 0:
            title_widget = layout.itemAt(0).widget()
            if isinstance(title_widget, QLabel):
                title_widget.setText(title)
    
    def get_user_info(self) -> str:
        """
        Obtiene la información actual del usuario
        
        Returns:
            str: Texto actual de la información del usuario
        """
        if self.user_info_label:
            return self.user_info_label.text()
        return "Usuario: No autenticado"
    
    def cleanup(self):
        """Limpia recursos cuando se cierra el widget"""
        if self.timer and self.timer.isActive():
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None
