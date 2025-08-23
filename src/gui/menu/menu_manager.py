"""
Manager para el sistema de menús de la aplicación
Centraliza toda la lógica de creación y configuración de menús
"""

from PySide6.QtGui import QAction


class MenuManager:
    """Gestor de menús para la ventana principal"""
    
    def __init__(self, main_window):
        """
        Inicializa el gestor de menús
        
        Args:
            main_window: Referencia a la ventana principal
        """
        self.main_window = main_window
        self.menubar = None
    
    def setup_menu(self):
        """Configura todos los menús de la aplicación"""
        self.menubar = self.main_window.menuBar()
        
        # Crear todos los menús
        self._create_file_menu()
        self._create_view_menu()
        self._create_tools_menu()
        self._create_help_menu()
    
    def _create_file_menu(self):
        """Crea el menú Archivo"""
        file_menu = self.menubar.addMenu("Archivo")
        
        # Nueva Alerta
        new_alert_action = QAction("Nueva Alerta", self.main_window)
        new_alert_action.setShortcut("Ctrl+N")
        new_alert_action.triggered.connect(
            lambda: self.main_window.tab_widget.setCurrentIndex(0)
        )
        file_menu.addAction(new_alert_action)
        
        file_menu.addSeparator()
        
        # Importar Excel
        import_action = QAction("Importar Excel...", self.main_window)
        import_action.triggered.connect(self.main_window.handle_import_excel)
        file_menu.addAction(import_action)
        
        # Exportar Excel
        export_action = QAction("Exportar Excel...", self.main_window)
        export_action.triggered.connect(self.main_window.handle_export_excel)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        # Salir
        exit_action = QAction("Salir", self.main_window)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.main_window.close)
        file_menu.addAction(exit_action)
    
    def _create_view_menu(self):
        """Crea el menú Ver"""
        view_menu = self.menubar.addMenu("Ver")
        
        # Dashboard
        dashboard_action = QAction("Dashboard", self.main_window)
        dashboard_action.setShortcut("Ctrl+D")
        dashboard_action.triggered.connect(
            lambda: self.main_window.tab_widget.setCurrentIndex(1)
        )
        view_menu.addAction(dashboard_action)
        
        # Gestión de Datos
        data_action = QAction("Gestión de Datos", self.main_window)
        data_action.triggered.connect(
            lambda: self.main_window.tab_widget.setCurrentIndex(2)
        )
        view_menu.addAction(data_action)
        
        view_menu.addSeparator()
        
        # Actualizar Dashboard
        refresh_action = QAction("Actualizar Dashboard", self.main_window)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.main_window.handle_refresh_dashboard)
        view_menu.addAction(refresh_action)
    
    def _create_tools_menu(self):
        """Crea el menú Herramientas"""
        tools_menu = self.menubar.addMenu("Herramientas")
        
        # Configuración
        settings_action = QAction("Configuración...", self.main_window)
        settings_action.triggered.connect(self.main_window.show_settings)
        tools_menu.addAction(settings_action)
        
        tools_menu.addSeparator()
        
        # Gestión de usuarios
        user_management_action = QAction("Gestión de Usuarios...", self.main_window)
        user_management_action.triggered.connect(self.main_window.show_user_management)
        tools_menu.addAction(user_management_action)
        
        tools_menu.addSeparator()
        
        # Actualizar estructura Excel
        update_excel_action = QAction("Actualizar Estructura Excel...", self.main_window)
        update_excel_action.triggered.connect(self.main_window.update_excel_structure)
        tools_menu.addAction(update_excel_action)
    
    def _create_help_menu(self):
        """Crea el menú Ayuda"""
        help_menu = self.menubar.addMenu("Ayuda")
        
        # Acerca de
        about_action = QAction("Acerca de...", self.main_window)
        about_action.triggered.connect(self.main_window.show_about)
        help_menu.addAction(about_action)
    
    # Métodos adicionales para gestión dinámica de menús si es necesario
    def enable_menu_item(self, menu_name, action_text, enabled=True):
        """
        Habilita/deshabilita un elemento específico del menú
        
        Args:
            menu_name: Nombre del menú
            action_text: Texto de la acción
            enabled: True para habilitar, False para deshabilitar
        """
        if not self.menubar:
            return
        
        for action in self.menubar.actions():
            if action.text() == menu_name:
                menu = action.menu()
                if menu:
                    for menu_action in menu.actions():
                        if menu_action.text() == action_text:
                            menu_action.setEnabled(enabled)
                            break
                break
    
    def set_menu_visible(self, menu_name, visible=True):
        """
        Muestra/oculta un menú completo
        
        Args:
            menu_name: Nombre del menú
            visible: True para mostrar, False para ocultar
        """
        if not self.menubar:
            return
        
        for action in self.menubar.actions():
            if action.text() == menu_name:
                action.setVisible(visible)
                break
    
    def configure_permissions(self, can_write, can_manage_users, can_delete):
        """
        Configura los permisos de los menús basados en el rol del usuario
        
        Args:
            can_write: Permiso de escritura
            can_manage_users: Permiso de gestión de usuarios
            can_delete: Permiso de eliminación
        """
        if not self.menubar:
            return
            
        # Configurar menú Archivo
        self.enable_menu_item("Archivo", "Nueva Alerta", can_write)
        self.enable_menu_item("Archivo", "Importar Excel...", can_write)
        self.enable_menu_item("Archivo", "Exportar Excel...", True)  # Siempre permitir exportar
        
        # Configurar menú Herramientas
        self.enable_menu_item("Herramientas", "Configuración", can_manage_users)
        self.enable_menu_item("Herramientas", "Gestión de Usuarios...", can_manage_users)
        self.enable_menu_item("Herramientas", "Actualizar Estructura Excel...", can_manage_users)
        self.enable_menu_item("Herramientas", "Limpiar Datos", can_delete)
        
        # Si no tiene permisos de escritura, cambiar textos para indicar solo lectura
        if not can_write:
            # Cambiar texto de menús para indicar restricciones
            for action in self.menubar.actions():
                if action.text() == "Archivo":
                    menu = action.menu()
                    if menu:
                        for menu_action in menu.actions():
                            if menu_action.text() == "Nueva Alerta":
                                menu_action.setText("📖 Nueva Alerta (Solo lectura)")
                            elif menu_action.text() == "Importar Excel...":
                                menu_action.setText("📖 Importar Excel... (Deshabilitado)")
                    break
