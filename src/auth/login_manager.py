""" Gestor de autenticación local con soporte para JSON y SQLite """
import json
import hashlib
import bcrypt
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QLineEdit, QPushButton, QMessageBox, QFormLayout, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# Importar estilos centralizados
from src.gui.styles import AuthStyles

class User:
    """Clase para representar un usuario"""
    def __init__(self, username: str, email: str = "", role: str = "user", created_at: str = None):
        self.username = username
        self.email = email
        self.role = role
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convierte el usuario a diccionario"""
        return {
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Crea un usuario desde un diccionario"""
        return cls(
            username=data["username"],
            email=data.get("email", ""),
            role=data.get("role", "user"),
            created_at=data.get("created_at")
        )

class AuthManager:
    """Gestor de autenticación local"""
    def __init__(self, data_file: str = "config/users.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(exist_ok=True, parents=True)
        self._ensure_data_file()

    def _ensure_data_file(self):
        """Asegura que el archivo de datos existe"""
        if not self.data_file.exists():
            default_data = {
                "users": {},
                "settings": {
                    "created_at": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
            # Crear usuario administrador por defecto
            admin_password = self._hash_password("admin123")
            default_data["users"]["admin"] = {
                "password_hash": admin_password,
                "user_info": User("admin", "admin@empresa.com", "admin").to_dict()
            }
            
            # Crear usuario de prueba con permisos de solo lectura
            demo_password = self._hash_password("demo123")
            default_data["users"]["demo"] = {
                "password_hash": demo_password,
                "user_info": User("demo", "demo@prueba.com", "viewer").to_dict()
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, indent=2, ensure_ascii=False)

    def _load_data(self) -> Dict:
        """Carga los datos del archivo"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando datos: {e}")
            return {"users": {}, "settings": {}}

    def _save_data(self, data: Dict):
        """Guarda los datos al archivo"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando datos: {e}")

    def _hash_password(self, password: str) -> str:
        """Hashea una contraseña usando bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verifica una contraseña contra su hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception:
            return False

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Autentica un usuario"""
        data = self._load_data()
        if username in data["users"]:
            user_data = data["users"][username]
            if self._verify_password(password, user_data["password_hash"]):
                return User.from_dict(user_data["user_info"])
        return None

    def create_user(self, username: str, password: str, email: str = "", role: str = "user") -> bool:
        """Crea un nuevo usuario"""
        data = self._load_data()
        if username in data["users"]:
            return False  # Usuario ya existe
        user = User(username, email, role)
        password_hash = self._hash_password(password)
        data["users"][username] = {
            "password_hash": password_hash,
            "user_info": user.to_dict()
        }
        self._save_data(data)
        return True

    def get_users(self) -> List[User]:
        """Obtiene la lista de usuarios"""
        data = self._load_data()
        users = []
        for user_data in data["users"].values():
            users.append(User.from_dict(user_data["user_info"]))
        return users

    def get_visible_users(self) -> List[User]:
        """Obtiene la lista de usuarios visibles en el login (excluye admin)"""
        data = self._load_data()
        users = []
        for username, user_data in data["users"].items():
            # Excluir usuario admin del login público
            if username != "admin":
                users.append(User.from_dict(user_data["user_info"]))
        return users

    def has_permission(self, user: User, permission: str) -> bool:
        """Verifica si un usuario tiene un permiso específico"""
        permissions = {
            "admin": ["read", "write", "delete", "manage_users", "admin_panel"],
            "user": ["read", "write"],
            "viewer": ["read"]  # Solo lectura
        }
        user_permissions = permissions.get(user.role, [])
        return permission in user_permissions

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Cambia la contraseña de un usuario"""
        data = self._load_data()
        if username not in data["users"]:
            return False
        user_data = data["users"][username]
        if not self._verify_password(old_password, user_data["password_hash"]):
            return False
        user_data["password_hash"] = self._hash_password(new_password)
        self._save_data(data)
        return True

class LoginDialog(QDialog):
    """Diálogo de login moderno y profesional"""
    def __init__(self, auth_manager: AuthManager):
        super().__init__()
        self.auth_manager = auth_manager
        self.current_user = None
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz del diálogo con diseño moderno y espaciado optimizado"""
        self.setWindowTitle("Inicio de Sesión - Sistema de Alertas Geotécnicas")
        self.setFixedSize(550, 750)
        self.setModal(True)

        # Aplicar estilos centralizados
        self.setStyleSheet(AuthStyles.get_complete_auth_styles())

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(25)
        layout.setContentsMargins(50, 0, 50, 0) # Margen: izq, arriba, der, abajo.

        # Header con título y subtítulo
        header_layout = QVBoxLayout()
        header_layout.setSpacing(15)
        header_layout.setAlignment(Qt.AlignCenter)

        # Título principal
        title = QLabel("Bienvenido")
        title.setAlignment(Qt.AlignCenter)
        title.setProperty("titleLabel", True)
        header_layout.addWidget(title)

        # Subtítulo
        subtitle = QLabel("Sistema de Alertas Geotécnicas")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setProperty("subtitleLabel", True)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setRowWrapPolicy(QFormLayout.WrapAllRows)

        # Campo Usuario
        user_label = QLabel("Nombre de Usuario")
        user_label.setProperty("fieldLabel", True)
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Ingrese su nombre de usuario")
        self.username_edit.setMinimumHeight(50)
        form_layout.addRow(user_label, self.username_edit)

        # Campo Contraseña
        password_label = QLabel("Contraseña")
        password_label.setProperty("fieldLabel", True)
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Ingrese su contraseña")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setMinimumHeight(50)
        form_layout.addRow(password_label, self.password_edit)
        layout.addLayout(form_layout)

        # Espaciado adicional antes de los botones principales
        layout.addSpacing(20)

        # Botones principales
        button_layout = QHBoxLayout()
        button_layout.setSpacing(25)
        button_layout.setAlignment(Qt.AlignCenter)

        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.setMinimumHeight(50)
        self.login_button.setProperty("loginButton", True)
        self.login_button.clicked.connect(self.login)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setMinimumHeight(50)
        self.cancel_button.setProperty("cancelButton", True)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        # Botones de gestión de cuentas
        account_buttons_layout = QHBoxLayout()
        account_buttons_layout.setSpacing(20)
        account_buttons_layout.setAlignment(Qt.AlignCenter)

        self.create_account_button = QPushButton("Crear Cuenta")
        self.create_account_button.setMinimumHeight(45)
        self.create_account_button.setProperty("createButton", True)
        self.create_account_button.clicked.connect(self.show_create_account)

        self.change_password_button = QPushButton("Cambiar Contraseña")
        self.change_password_button.setMinimumHeight(45)
        self.change_password_button.setProperty("changePasswordButton", True)
        self.change_password_button.clicked.connect(self.show_change_password)
        account_buttons_layout.addWidget(self.create_account_button)
        account_buttons_layout.addWidget(self.change_password_button)
        layout.addLayout(account_buttons_layout)

        # Conectar Enter para login
        self.username_edit.returnPressed.connect(self.login)
        self.password_edit.returnPressed.connect(self.login)

        # Foco inicial
        self.username_edit.setFocus()

        # Información de usuario demo
        info_label = QLabel("Usuario de prueba: demo / demo123 (Solo lectura)")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setProperty("infoLabel", True)
        layout.addWidget(info_label)

        # Botón de acceso admin (discreto)
        admin_access_layout = QHBoxLayout()
        admin_access_layout.setAlignment(Qt.AlignCenter)
        admin_access_layout.setContentsMargins(0, 10, 0, 0)
        
        self.admin_access_button = QPushButton("Acceso Administrador")
        self.admin_access_button.setMinimumHeight(35)
        self.admin_access_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 11px;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
            }
        """)
        self.admin_access_button.clicked.connect(self.show_admin_login)
        admin_access_layout.addWidget(self.admin_access_button)
        layout.addLayout(admin_access_layout)

        # Estilo global para QMessageBox (texto negro)
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            current_style = app.styleSheet()
            app.setStyleSheet(current_style + """
                QMessageBox {
                    background-color: white;
                    color: black;
                }
                QMessageBox QLabel {
                    color: black;
                    font-size: 12px;
                    font-family: 'Segoe UI';
                }
                QMessageBox QPushButton {
                    background-color: #f0f0f0;
                    color: black;
                    border: 1px solid #ccc;
                    padding: 5px 15px;
                    border-radius: 3px;
                    font-family: 'Segoe UI';
                }
                QMessageBox QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QMessageBox QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)

    def login(self):
        """Procesa el login"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor ingrese usuario y contraseña")
            return
        user = self.auth_manager.authenticate(username, password)
        if user:
            self.current_user = user
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")
            self.password_edit.clear()
            self.username_edit.setFocus()

    def show_admin_login(self):
        """Muestra un diálogo específico para acceso de administrador"""
        dialog = AdminLoginDialog(self.auth_manager, self)
        if dialog.exec() == QDialog.Accepted:
            self.current_user = dialog.current_user
            self.accept()

    def show_create_account(self):
        """Muestra el diálogo para crear cuenta"""
        # Verificar si hay un usuario actual logueado y si es admin
        is_admin = False
        if hasattr(self, 'current_user') and self.current_user and self.current_user.role == "admin":
            is_admin = True
            
        dialog = CreateAccountDialog(self.auth_manager, self, is_admin)
        if dialog.exec() == QDialog.Accepted:
            QMessageBox.information(self, "Éxito", "Cuenta creada correctamente")

    def show_change_password(self):
        """Muestra el diálogo para cambiar contraseña"""
        dialog = ChangePasswordDialog(self.auth_manager, self)
        if dialog.exec() == QDialog.Accepted:
            QMessageBox.information(self, "Éxito", "Contraseña cambiada correctamente")

class AdminLoginDialog(QDialog):
    """Diálogo específico para acceso de administrador"""
    def __init__(self, auth_manager: AuthManager, parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.current_user = None
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz del diálogo de admin"""
        self.setWindowTitle("Acceso de Administrador")
        self.setFixedSize(400, 350)
        self.setModal(True)

        # Aplicar estilos específicos para admin
        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #8B0000,
                    stop: 1 #DC143C
                );
                border-radius: 15px;
            }}
            QLabel {{
                color: white;
                font-family: 'Segoe UI';
                border: none;
                background: transparent;
            }}
            QLineEdit {{
                background-color: rgba(255, 255, 255, 0.95);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                color: #333;
                font-family: 'Segoe UI';
            }}
            QLineEdit:focus {{
                border: 2px solid #FFD700;
                background-color: white;
            }}
            QPushButton {{
                background-color: #8B0000;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: #A0522D;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Título
        title = QLabel("Acceso de Administrador")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        # Advertencia
        warning = QLabel("⚠️ Acceso restringido al personal autorizado")
        warning.setAlignment(Qt.AlignCenter)
        warning.setStyleSheet("font-size: 12px; color: #FFD700; margin-bottom: 15px;")
        layout.addWidget(warning)

        # Formulario
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Usuario
        user_label = QLabel("Usuario Administrador:")
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("admin")
        form_layout.addWidget(user_label)
        form_layout.addWidget(self.username_edit)

        # Contraseña
        password_label = QLabel("Contraseña:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("Contraseña de administrador")
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_edit)

        layout.addLayout(form_layout)

        # Botones
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignCenter)

        self.login_button = QPushButton("Acceder")
        self.login_button.clicked.connect(self.admin_login)
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        # Conectar Enter
        self.username_edit.returnPressed.connect(self.admin_login)
        self.password_edit.returnPressed.connect(self.admin_login)
        self.username_edit.setFocus()

    def admin_login(self):
        """Procesa el login de administrador"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor ingrese usuario y contraseña")
            return
            
        # Solo permitir usuarios con rol admin
        user = self.auth_manager.authenticate(username, password)
        if user and user.role == "admin":
            self.current_user = user
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Acceso denegado. Solo administradores autorizados.")
            self.password_edit.clear()
            self.username_edit.setFocus()

class CreateAccountDialog(QDialog):
    """Diálogo para crear nueva cuenta con diseño profesional"""
    def __init__(self, auth_manager: AuthManager, parent=None, is_admin_user=False):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.is_admin_user = is_admin_user
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz del diálogo con diseño moderno y colores Teck"""
        self.setWindowTitle("Crear Nueva Cuenta")
        self.setFixedSize(450, 550)
        self.setModal(True)

        # Aplicar estilos usando el sistema centralizado
        self.setStyleSheet(AuthStyles.get_registration_dialog_styles() + AuthStyles.get_input_styles())

        layout = QVBoxLayout(self)
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)

        # Título
        title = QLabel("Crear Nueva Cuenta")
        title.setProperty("registrationTitle", True)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.setLabelAlignment(Qt.AlignLeft)

        # Campo Usuario
        user_label = QLabel("Usuario")
        user_label.setProperty("registrationField", True)
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Nombre de usuario único")
        form_layout.addRow(user_label, self.username_edit)

        # Campo Email
        email_label = QLabel("Email")
        email_label.setProperty("registrationField", True)
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("correo@empresa.com")
        form_layout.addRow(email_label, self.email_edit)

        # Campo Contraseña
        password_label = QLabel("Contraseña")
        password_label.setProperty("registrationField", True)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("Mínimo 6 caracteres")
        form_layout.addRow(password_label, self.password_edit)

        # Campo Confirmar Contraseña
        confirm_label = QLabel("Confirmar Contraseña")
        confirm_label.setProperty("registrationField", True)
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_password_edit.setPlaceholderText("Repetir contraseña")
        form_layout.addRow(confirm_label, self.confirm_password_edit)

        # Campo Rol
        role_label = QLabel("Rol")
        role_label.setProperty("registrationField", True)
        self.role_combo = QComboBox()
        
        # Solo administradores pueden crear otros administradores
        if self.is_admin_user:
            self.role_combo.addItems(["user", "admin"])
            role_info = QLabel("ℹ️ Como administrador, puede crear usuarios con cualquier rol")
            role_info.setStyleSheet("color: #28a745; font-size: 12px; margin-top: 5px;")
        else:
            self.role_combo.addItems(["user"])
            role_info = QLabel("ℹ️ Solo se pueden crear usuarios estándar. Para crear administradores, contacte a un administrador del sistema.")
            role_info.setStyleSheet("color: #6c757d; font-size: 12px; margin-top: 5px;")
            
        form_layout.addRow(role_label, self.role_combo)
        form_layout.addRow("", role_info)  # Agregar info en fila separada
        layout.addLayout(form_layout)

        # Botones
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignCenter)

        self.create_button = QPushButton("Crear Cuenta")
        self.create_button.setProperty("registerButton", True)
        self.create_button.setMinimumHeight(50)
        self.create_button.clicked.connect(self.create_account)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setProperty("registerCancelButton", True)
        self.cancel_button.setMinimumHeight(50)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def create_account(self):
        """Crea la nueva cuenta"""
        username = self.username_edit.text().strip()
        email = self.email_edit.text().strip()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()
        role = self.role_combo.currentText()

        # Validaciones
        if not username:
            QMessageBox.warning(self, "Error", "El nombre de usuario es obligatorio")
            return
        if len(username) < 3:
            QMessageBox.warning(self, "Error", "El nombre de usuario debe tener al menos 3 caracteres")
            return
        if not password:
            QMessageBox.warning(self, "Error", "La contraseña es obligatoria")
            return
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "La contraseña debe tener al menos 6 caracteres")
            return
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            return

        # Crear usuario
        if self.auth_manager.create_user(username, password, email, role):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "El usuario ya existe")

class ChangePasswordDialog(QDialog):
    """Diálogo para cambiar contraseña con diseño profesional"""
    def __init__(self, auth_manager: AuthManager, parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz del diálogo con diseño moderno"""
        self.setWindowTitle("Cambiar Contraseña")
        self.setFixedSize(450, 500)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QLabel {
                color: #2c3e50;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)

        # Título
        title = QLabel("Cambiar Contraseña")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)

        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.setLabelAlignment(Qt.AlignLeft)

        label_style = """
            QLabel {
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: 500;
                color: #495057;
                margin-bottom: 6px;
            }
        """
        input_style = """
            QLineEdit {
                padding: 14px 18px;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                font-size: 15px;
                font-family: 'Segoe UI';
                background-color: white;
                min-height: 40px;
            }
            QLineEdit:focus {
                border-color: #007bff;
                outline: none;
            }
            QLineEdit:hover {
                border-color: #ced4da;
            }
            QLineEdit::placeholder {
                color: #6c757d;
                font-style: italic;
            }
        """

        # Campo Usuario
        user_label = QLabel("Usuario")
        user_label.setStyleSheet(label_style)
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Nombre de usuario")
        self.username_edit.setStyleSheet(input_style)
        form_layout.addRow(user_label, self.username_edit)

        # Campo Contraseña Actual
        old_pass_label = QLabel("Contraseña Actual")
        old_pass_label.setStyleSheet(label_style)
        self.old_password_edit = QLineEdit()
        self.old_password_edit.setEchoMode(QLineEdit.Password)
        self.old_password_edit.setPlaceholderText("Contraseña actual")
        self.old_password_edit.setStyleSheet(input_style)
        form_layout.addRow(old_pass_label, self.old_password_edit)

        # Campo Nueva Contraseña
        new_pass_label = QLabel("Nueva Contraseña")
        new_pass_label.setStyleSheet(label_style)
        self.new_password_edit = QLineEdit()
        self.new_password_edit.setEchoMode(QLineEdit.Password)
        self.new_password_edit.setPlaceholderText("Nueva contraseña (mín. 6 caracteres)")
        self.new_password_edit.setStyleSheet(input_style)
        form_layout.addRow(new_pass_label, self.new_password_edit)

        # Campo Confirmar Nueva Contraseña
        confirm_label = QLabel("Confirmar Nueva Contraseña")
        confirm_label.setStyleSheet(label_style)
        self.confirm_new_password_edit = QLineEdit()
        self.confirm_new_password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_new_password_edit.setPlaceholderText("Repetir nueva contraseña")
        self.confirm_new_password_edit.setStyleSheet(input_style)
        form_layout.addRow(confirm_label, self.confirm_new_password_edit)
        layout.addLayout(form_layout)

        # Botones
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignCenter)

        self.change_button = QPushButton("Cambiar Contraseña")
        self.change_button.setMinimumHeight(50)
        self.change_button.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                padding: 14px 28px;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 600;
                font-family: 'Segoe UI';
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
            QPushButton:pressed {
                background-color: #10707f;
            }
        """)
        self.change_button.clicked.connect(self.change_password)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setMinimumHeight(50)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 14px 28px;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 600;
                font-family: 'Segoe UI';
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
            QPushButton:pressed {
                background-color: #494f54;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.change_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def change_password(self):
        """Cambia la contraseña"""
        username = self.username_edit.text().strip()
        old_password = self.old_password_edit.text()
        new_password = self.new_password_edit.text()
        confirm_new_password = self.confirm_new_password_edit.text()

        # Validaciones
        if not username:
            QMessageBox.warning(self, "Error", "El nombre de usuario es obligatorio")
            return
        if not old_password:
            QMessageBox.warning(self, "Error", "La contraseña actual es obligatoria")
            return
        if not new_password:
            QMessageBox.warning(self, "Error", "La nueva contraseña es obligatoria")
            return
        if len(new_password) < 6:
            QMessageBox.warning(self, "Error", "La nueva contraseña debe tener al menos 6 caracteres")
            return
        if new_password != confirm_new_password:
            QMessageBox.warning(self, "Error", "Las nuevas contraseñas no coinciden")
            return

        # Cambiar contraseña
        if self.auth_manager.change_password(username, old_password, new_password):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Usuario no encontrado o contraseña actual incorrecta")

class LoginManager:
    """Gestor de login que integra el diálogo de autenticación"""
    def __init__(self):
        self.auth_manager = AuthManager()
        self.current_user = None

    def show_login(self) -> bool:
        """Muestra el diálogo de login y retorna True si el login fue exitoso"""
        dialog = LoginDialog(self.auth_manager)
        if dialog.exec() == QDialog.Accepted:
            self.current_user = dialog.current_user
            return True
        return False

    def get_current_user(self):
        """Retorna el usuario actual autenticado"""
        return self.current_user

    def logout(self):
        """Cierra la sesión del usuario actual"""
        self.current_user = None

    def show_create_user_dialog(self, parent=None) -> bool:
        """Muestra el diálogo para crear usuario desde la aplicación (con usuario logueado)"""
        if not self.current_user:
            return False
            
        is_admin = self.current_user.role == "admin"
        dialog = CreateAccountDialog(self.auth_manager, parent, is_admin)
        
        if dialog.exec() == QDialog.Accepted:
            return True
        return False