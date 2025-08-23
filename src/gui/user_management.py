"""
Diálogo para gestión de usuarios
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTableWidget, QTableWidgetItem,
                              QMessageBox, QHeaderView, QMenu, QAbstractItemView)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QAction, QContextMenuEvent
from datetime import datetime

from src.auth.login_manager import AuthManager, CreateAccountDialog, ChangePasswordDialog


class UserTableWidget(QTableWidget):
    """Tabla personalizada para usuarios con menú contextual"""
    
    user_deleted = Signal(str)  # Señal emitida cuando se elimina un usuario
    
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        self.setup_table()
        self.load_users()
        
    def setup_table(self):
        """Configura la tabla"""
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Usuario", "Email", "Rol", "Fecha Creación"])
        
        # Configurar selección
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # Ajustar columnas
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        # Estilos modernos con buen contraste
        self.setAlternatingRowColors(True)
        self.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                gridline-color: #e9ecef;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                selection-background-color: #007bff;
                selection-color: #ffffff;
                alternate-background-color: #f8f9fa;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #e9ecef;
                color: #212529;
            }
            QTableWidget::item:selected {
                background-color: #007bff;
                color: #ffffff;
            }
            QTableWidget::item:hover {
                background-color: #e9ecef;
                color: #212529;
            }
            QHeaderView::section {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #4CAF50,
                    stop: 1 #45a049
                );
                color: #ffffff;
                border: 1px solid #45a049;
                padding: 12px 8px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                text-align: left;
            }
            QHeaderView::section:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #45a049,
                    stop: 1 #3d8b40
                );
            }
        """)
        
    def load_users(self):
        """Carga los usuarios en la tabla"""
        from PySide6.QtGui import QColor
        
        users = self.auth_manager.get_users()
        self.setRowCount(len(users))
        
        for row, user in enumerate(users):
            # Usuario
            username_item = QTableWidgetItem(user.username)
            if user.role == "admin":
                username_item.setFont(QFont("Segoe UI", 11, QFont.Bold))
                username_item.setForeground(QColor("#dc3545"))  # Rojo para destacar admin
                
            self.setItem(row, 0, username_item)
            
            # Email
            email_item = QTableWidgetItem(user.email)
            if user.role == "admin":
                email_item.setForeground(QColor("#dc3545"))
            self.setItem(row, 1, email_item)
            
            # Rol
            role_item = QTableWidgetItem(user.role.upper())
            if user.role == "admin":
                role_item.setBackground(QColor("#fff3cd"))  # Fondo amarillo claro
                role_item.setForeground(QColor("#856404"))  # Texto marrón oscuro
                role_item.setFont(QFont("Segoe UI", 11, QFont.Bold))
            else:
                role_item.setForeground(QColor("#6f42c1"))  # Púrpura para usuarios normales
                role_item.setFont(QFont("Segoe UI", 11, QFont.Normal))
                
            self.setItem(row, 2, role_item)
            
            # Fecha creación
            try:
                created_date = datetime.fromisoformat(user.created_at)
                date_str = created_date.strftime("%d/%m/%Y %H:%M")
            except:
                date_str = user.created_at or "N/A"
                
            date_item = QTableWidgetItem(date_str)
            if user.role == "admin":
                date_item.setForeground(QColor("#dc3545"))
            self.setItem(row, 3, date_item)
            
    def contextMenuEvent(self, event: QContextMenuEvent):
        """Muestra el menú contextual"""
        if self.itemAt(event.pos()) is None:
            return
            
        menu = QMenu(self)
        
        # Obtener usuario seleccionado
        current_row = self.currentRow()
        if current_row < 0:
            return
            
        username = self.item(current_row, 0).text()
        user_role = self.item(current_row, 2).text()
        
        # Acciones del menú
        change_password_action = QAction("Cambiar Contraseña", self)
        change_password_action.triggered.connect(lambda: self.change_user_password(username))
        menu.addAction(change_password_action)
        
        if user_role != "admin" or username != "admin":  # No permitir eliminar admin principal
            delete_action = QAction("Eliminar Usuario", self)
            delete_action.triggered.connect(lambda: self.delete_user(username))
            menu.addAction(delete_action)
            
        menu.exec(event.globalPos())
        
    def change_user_password(self, username: str):
        """Cambia la contraseña de un usuario específico"""
        dialog = ChangePasswordDialog(self.auth_manager, self)
        dialog.username_edit.setText(username)
        dialog.username_edit.setReadOnly(True)
        
        if dialog.exec() == QDialog.Accepted:
            QMessageBox.information(self, "Éxito", f"Contraseña de {username} cambiada correctamente")
            
    def delete_user(self, username: str):
        """Elimina un usuario"""
        reply = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar el usuario '{username}'?\n\n"
            "Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Cargar datos
                data = self.auth_manager._load_data()
                
                if username in data["users"]:
                    del data["users"][username]
                    self.auth_manager._save_data(data)
                    
                    QMessageBox.information(self, "Éxito", f"Usuario '{username}' eliminado correctamente")
                    self.load_users()  # Recargar tabla
                    self.user_deleted.emit(username)
                else:
                    QMessageBox.warning(self, "Error", "Usuario no encontrado")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error eliminando usuario: {str(e)}")


class UserManagementDialog(QDialog):
    """Diálogo principal para gestión de usuarios"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_manager = AuthManager()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        self.setWindowTitle("Gestión de Usuarios")
        self.setModal(True)
        self.resize(700, 500)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("Gestión de Usuarios del Sistema")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        self.create_user_button = QPushButton("Crear Usuario")
        self.create_user_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.create_user_button.clicked.connect(self.create_user)
        
        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.refresh_button.clicked.connect(self.refresh_users)
        
        button_layout.addWidget(self.create_user_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Tabla de usuarios
        self.user_table = UserTableWidget()
        self.user_table.user_deleted.connect(self.on_user_deleted)
        layout.addWidget(self.user_table)
        
        # Información
        info_label = QLabel("Haga clic derecho en un usuario para ver opciones adicionales")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #666; font-style: italic; margin-top: 10px;")
        layout.addWidget(info_label)
        
        # Estadísticas
        self.stats_label = QLabel()
        self.update_stats()
        layout.addWidget(self.stats_label)
        
        # Botón cerrar
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        
        self.close_button = QPushButton("Cerrar")
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.close_button.clicked.connect(self.accept)
        
        close_layout.addWidget(self.close_button)
        layout.addLayout(close_layout)
        
    def create_user(self):
        """Abre el diálogo para crear usuario"""
        dialog = CreateAccountDialog(self.auth_manager, self)
        
        if dialog.exec() == QDialog.Accepted:
            QMessageBox.information(self, "Éxito", "Usuario creado correctamente")
            self.refresh_users()
            
    def refresh_users(self):
        """Actualiza la lista de usuarios"""
        self.user_table.load_users()
        self.update_stats()
        
    def update_stats(self):
        """Actualiza las estadísticas"""
        users = self.auth_manager.get_users()
        total_users = len(users)
        admin_users = len([u for u in users if u.role == "admin"])
        regular_users = total_users - admin_users
        
        stats_text = f"Total de usuarios: {total_users} | Administradores: {admin_users} | Usuarios regulares: {regular_users}"
        self.stats_label.setText(stats_text)
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("color: #2E8B57; font-weight: bold; padding: 10px;")
        
    def on_user_deleted(self, username: str):
        """Maneja cuando se elimina un usuario"""
        self.update_stats()
