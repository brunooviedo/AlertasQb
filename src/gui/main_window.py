"""
Ventana principal de la aplicación de alertas geotécnicas
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QTabWidget, QStatusBar, QMessageBox, QSizePolicy)
from PySide6.QtCore import Qt
from datetime import datetime

# Imports lazy - se cargan solo cuando se necesitan
from src.gui.styles.main_styles import MainWindowStyles
from src.gui.menu.menu_manager import MenuManager
from src.gui.components.header_widget import HeaderWidget
from src.auth.login_manager import User

# Componentes pesados se importan dinámicamente
_alert_form = None
_dashboard = None
_data_manager = None
_alerts_viewer = None
_settings_dialog = None
_about_dialog = None

def _get_alert_form():
    """Carga lazy del formulario de alertas"""
    global _alert_form
    if _alert_form is None:
        from src.gui.alert_form import AlertForm
        _alert_form = AlertForm
    return _alert_form()

def _get_dashboard():
    """Carga lazy del dashboard"""
    global _dashboard
    if _dashboard is None:
        from src.gui.dashboard import Dashboard
        _dashboard = Dashboard
        print("✓ Dashboard cargado dinámicamente")
    return _dashboard()

def _get_data_manager():
    """Carga lazy del gestor de datos"""
    global _data_manager
    if _data_manager is None:
        from src.gui.data_manager_new import DataManagerWidget
        _data_manager = DataManagerWidget
    return _data_manager()

def _get_alerts_viewer():
    """Carga lazy del visualizador de alertas"""
    global _alerts_viewer
    if _alerts_viewer is None:
        from src.gui.alerts_data_viewer import AlertsDataViewer
        _alerts_viewer = AlertsDataViewer
    return _alerts_viewer()

def _get_settings_dialog():
    """Carga lazy del diálogo de configuración"""
    global _settings_dialog
    if _settings_dialog is None:
        from src.gui.settings_dialog import SettingsDialog
        _settings_dialog = SettingsDialog
    return _settings_dialog

def _get_about_dialog():
    """Carga lazy del diálogo acerca de"""
    global _about_dialog
    if _about_dialog is None:
        from src.gui.about_dialog import AboutDialog
        _about_dialog = AboutDialog
    return _about_dialog


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        
        # Inicializar el gestor de menús
        self.menu_manager = MenuManager(self)
        
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()
        self.apply_styles()
        
    def setup_ui(self):
        """Configura la interfaz principal"""
        self.setWindowTitle("Sistema de Alertas Geotécnicas")
        
        # Configurar ventana para que se abra maximizada
        self.setMinimumSize(1200, 800)  # Tamaño mínimo
        self.showMaximized()  # Abrir maximizada por defecto
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal con configuración responsiva
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # Header con información del usuario
        self.header_frame = HeaderWidget(self)
        main_layout.addWidget(self.header_frame)
        
        # Tabs principales - carga lazy
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setSizePolicy(QSizePolicy.Policy.Expanding, 
                                     QSizePolicy.Policy.Expanding)
        
        # Solo crear la primera tab inicialmente (Nueva Alerta)
        self.alert_form = _get_alert_form()
        self.tab_widget.addTab(self.alert_form, "Nueva Alerta")
        
        # Crear tabs placeholder que se cargan dinámicamente
        self.dashboard = None
        self.alerts_data_viewer = None
        self.data_manager = None
        
        # Añadir tabs con widgets temporales
        self.tab_widget.addTab(QWidget(), "Dashboard")
        self.tab_widget.addTab(QWidget(), "Datos de Alertas")
        self.tab_widget.addTab(QWidget(), "Gestión de Datos")
        
        # Conectar evento para carga lazy de tabs
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        main_layout.addWidget(self.tab_widget)
        
        # Conectar señales
        self.alert_form.alert_saved.connect(self.on_alert_saved)
        

    def setup_menu(self):
        """Configura el menú principal utilizando MenuManager"""
        self.menu_manager.setup_menu()
        
    def setup_status_bar(self):
        """Configura la barra de estado"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.status_bar.showMessage("Listo", 2000)
        
    def apply_styles(self):
        """Aplica estilos modernos a la aplicación"""
        self.setStyleSheet(MainWindowStyles.get_complete_styles())
        
    def set_current_user(self, user: User):
        """Establece el usuario actual y configura permisos"""
        self.current_user = user
        self.header_frame.set_user_info(user.username, user.role)
        
        # Pasar el usuario a los componentes que lo necesiten
        self.alert_form.set_current_user(user)
        
        # Configurar permisos basados en el rol
        self.configure_user_permissions(user)
        
    def configure_user_permissions(self, user: User):
        """Configura los permisos de la interfaz basados en el rol del usuario"""
        from src.auth.login_manager import AuthManager
        auth_manager = AuthManager()
        
        # Verificar permisos de escritura
        can_write = auth_manager.has_permission(user, "write")
        can_manage_users = auth_manager.has_permission(user, "manage_users")
        can_delete = auth_manager.has_permission(user, "delete")
        
        # Configurar tabs según permisos
        if not can_write:
            # Usuario viewer: habilitar pestaña pero cambiar texto a solo lectura
            self.tab_widget.setTabText(0, "📊 Formulario (Solo lectura)")
            
            # Configurar botones del formulario de alertas para solo lectura
            self.configure_alert_form_permissions(can_write)
            
            # Deshabilitar gestión de datos si no puede escribir
            if hasattr(self, 'data_manager_tab_index'):
                self.tab_widget.setTabEnabled(self.data_manager_tab_index, False)
        else:
            # Usuario con permisos de escritura: habilitar todos los botones
            self.configure_alert_form_permissions(can_write)
        
        # Configurar menús según permisos
        if hasattr(self, 'menu_manager'):
            self.menu_manager.configure_permissions(can_write, can_manage_users, can_delete)
            
        # Mostrar información del usuario en status bar
        permission_text = "Solo lectura" if not can_write else "Lectura/Escritura"
        if user.role == "admin":
            permission_text = "Administrador completo"
            
        self.statusBar().showMessage(f"Usuario: {user.username} ({user.role}) - {permission_text}", 5000)
    
    def on_tab_changed(self, index):
        """Carga lazy de tabs cuando el usuario hace click en ellas"""
        if index == 1 and self.dashboard is None:  # Dashboard tab
            print("🔄 Cargando Dashboard...")
            self.dashboard = _get_dashboard()
            self.tab_widget.removeTab(1)
            self.tab_widget.insertTab(1, self.dashboard, "Dashboard")
            self.tab_widget.setCurrentIndex(1)
            # Conectar señal de alerta guardada
            if hasattr(self, 'alert_form'):
                self.alert_form.alert_saved.connect(self.dashboard.refresh_charts)
                
        elif index == 2 and self.alerts_data_viewer is None:  # Datos de alertas tab
            print("🔄 Cargando Visor de Datos...")
            self.alerts_data_viewer = _get_alerts_viewer()
            self.tab_widget.removeTab(2)
            self.tab_widget.insertTab(2, self.alerts_data_viewer, "Datos de Alertas")
            self.tab_widget.setCurrentIndex(2)
            # Conectar señal de alerta guardada
            if hasattr(self, 'alert_form'):
                self.alert_form.alert_saved.connect(self.alerts_data_viewer.load_data)
                
        elif index == 3 and self.data_manager is None:  # Gestión de datos tab
            print("🔄 Cargando Gestión de Datos...")
            self.data_manager = _get_data_manager()
            self.tab_widget.removeTab(3)
            self.tab_widget.insertTab(3, self.data_manager, "Gestión de Datos")
            self.tab_widget.setCurrentIndex(3)
        

    def on_alert_saved(self, alert_data):
        """Maneja cuando se guarda una alerta"""
        self.status_bar.showMessage(f"Alerta guardada: {alert_data['TipoAlerta']}", 3000)
        
        # Actualizar dashboard solo si ya está cargado
        if self.dashboard is not None:
            self.dashboard.refresh_charts()
        
        # Actualizar visor de datos solo si ya está cargado
        if self.alerts_data_viewer is not None:
            self.alerts_data_viewer.load_data()
        
        # Mostrar notificación para alertas rojas
        if alert_data['TipoAlerta'] == 'Roja':
            QMessageBox.information(
                self, 
                "Alerta Roja Registrada",
                f"Se ha registrado una alerta roja.\n\n"
                f"Condición: {alert_data['Condicion']}\n"
                f"Hora: {alert_data['FechaHora']}"
            )
    
    def handle_import_excel(self):
        """Maneja la importación de Excel - carga lazy del data_manager"""
        if self.data_manager is None:
            # Cargar data_manager si no existe y cambiar a esa tab
            self.tab_widget.setCurrentIndex(3)  # Esto triggerará la carga lazy
        if self.data_manager is not None:
            self.data_manager.import_excel()
    
    def handle_export_excel(self):
        """Maneja la exportación de Excel - carga lazy del data_manager"""
        if self.data_manager is None:
            # Cargar data_manager si no existe y cambiar a esa tab
            self.tab_widget.setCurrentIndex(3)  # Esto triggerará la carga lazy
        if self.data_manager is not None:
            self.data_manager.export_excel()
            
    def handle_refresh_dashboard(self):
        """Maneja la actualización del dashboard - carga lazy del dashboard"""
        if self.dashboard is None:
            # Cargar dashboard si no existe y cambiar a esa tab
            self.tab_widget.setCurrentIndex(1)  # Esto triggerará la carga lazy
        if self.dashboard is not None:
            self.dashboard.refresh_charts()
            
    def show_settings(self):
        """Muestra el diálogo de configuración"""
        dialog = _get_settings_dialog()(self)
        dialog.exec()
        
    def show_user_management(self):
        """Muestra el diálogo de gestión de usuarios (solo para administradores)"""
        # Verificar que hay un usuario actual y que es administrador
        if not hasattr(self, 'current_user') or not self.current_user:
            QMessageBox.warning(self, "Acceso Denegado", "No hay usuario autenticado.")
            return
            
        if self.current_user.role != "admin":
            QMessageBox.warning(self, "Acceso Denegado", 
                              "Solo los administradores pueden acceder a la gestión de usuarios.")
            return
            
        from src.gui.user_management import UserManagementDialog
        dialog = UserManagementDialog(self)
        dialog.exec()
        
    def update_excel_structure(self):
        """Actualiza la estructura del archivo Excel añadiendo columnas faltantes"""
        try:
            from src.data.excel_manager import ExcelManager
            
            # Mostrar diálogo de confirmación
            reply = QMessageBox.question(
                self, 
                "Actualizar Estructura Excel",
                "¿Desea actualizar la estructura del archivo Excel para incluir las nuevas columnas (Ubicación y Velocidad mm/día)?\n\n"
                "Esta operación:\n"
                "• Añadirá las columnas faltantes con valores por defecto\n"
                "• No eliminará datos existentes\n"
                "• Reordenará las columnas según el formato actual",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                excel_manager = ExcelManager()
                success = excel_manager.update_excel_structure()
                
                if success:
                    QMessageBox.information(
                        self, 
                        "Éxito", 
                        "La estructura del archivo Excel ha sido actualizada correctamente.\n\n"
                        "Las nuevas columnas 'Ubicación' y 'Velocidad mm/día' están ahora disponibles."
                    )
                    # Recargar datos en todas las pestañas
                    if hasattr(self, 'alerts_data_viewer'):
                        self.alerts_data_viewer.load_data()
                    if hasattr(self, 'dashboard'):
                        self.dashboard.load_data()
                else:
                    QMessageBox.warning(
                        self, 
                        "Error", 
                        "No se pudo actualizar la estructura del archivo Excel.\n"
                        "Verifique que el archivo no esté abierto en otro programa."
                    )
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error", 
                f"Error al actualizar la estructura del Excel:\n{str(e)}"
            )
        
    def show_about(self):
        """Muestra información sobre la aplicación"""
        _get_about_dialog().show_about(self)
        
    def closeEvent(self, event):
        """Maneja el cierre de la aplicación"""
        reply = QMessageBox.question(
            self, 
            "Confirmar Salida", 
            "¿Está seguro de que desea salir?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def configure_alert_form_permissions(self, can_write):
        """Configura los permisos de los botones del formulario de alertas y datos de alertas"""
        # Configurar formulario de alertas (primera pestaña)
        if self.tab_widget.count() > 0:
            alert_form_widget = self.tab_widget.widget(0)
            
            # Si el widget es un AlertForm, configurar sus botones
            if hasattr(alert_form_widget, 'save_button'):
                alert_form_widget.save_button.setEnabled(can_write)
                
            if hasattr(alert_form_widget, 'clear_button'):
                alert_form_widget.clear_button.setEnabled(can_write)
                
            if hasattr(alert_form_widget, 'edit_button'):
                alert_form_widget.edit_button.setEnabled(can_write)
                
            if hasattr(alert_form_widget, 'delete_button'):
                alert_form_widget.delete_button.setEnabled(can_write)
                
            # Si hay botones de agregar/modificar en el formulario
            if hasattr(alert_form_widget, 'add_button'):
                alert_form_widget.add_button.setEnabled(can_write)
                
            # Deshabilitar campos de entrada para usuarios de solo lectura
            if not can_write and hasattr(alert_form_widget, 'set_read_only'):
                alert_form_widget.set_read_only(True)
        
        # Configurar pestaña de datos de alertas (tercera pestaña - índice 2)
        if self.tab_widget.count() > 2:
            alerts_data_widget = self.tab_widget.widget(2)
            
            # Configurar botones de AlertsDataViewer
            if hasattr(alerts_data_widget, 'delete_button'):
                alerts_data_widget.delete_button.setEnabled(can_write)
                
            # El botón de exportar siempre debe estar habilitado
            if hasattr(alerts_data_widget, 'export_button'):
                alerts_data_widget.export_button.setEnabled(True)
                
            # El botón de actualizar siempre debe estar habilitado
            if hasattr(alerts_data_widget, 'refresh_button'):
                alerts_data_widget.refresh_button.setEnabled(True)
                
            # Configurar modo solo lectura si el widget lo soporta
            if not can_write and hasattr(alerts_data_widget, 'set_read_only'):
                alerts_data_widget.set_read_only(True)
