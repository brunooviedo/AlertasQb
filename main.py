"""
Aplicación GUI para Registro de Alertas Geotécnicas
Sistema completo con autenticación, almacenamiento en Excel y dashboard
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Importaciones mínimas para arranque ultra-rápido
from PySide6.QtWidgets import QApplication, QSplashScreen, QLabel
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt, QTimer

# Importar configuración de versión
from src.utils.version import APP_VERSION, UPDATE_SERVER_URL, UPDATE_CHECK_ON_STARTUP


def create_splash_screen():
    """Crear splash screen minimalista para carga rápida"""
    # Crear splash screen simple sin imágenes
    splash = QSplashScreen()
    splash.setFixedSize(400, 200)
    
    # Configurar apariencia moderna
    splash.setStyleSheet("""
        QSplashScreen {
            background-color: #3153E4;
            border: 2px solid #00A26A;
            border-radius: 10px;
        }
    """)
    
    # Agregar texto
    splash.showMessage("� AlertasQB - Cargando...", 
                      Qt.AlignCenter | Qt.AlignBottom, 
                      Qt.white)
    
    return splash


def check_updates_during_startup(splash, app):
    """Verificar actualizaciones durante el splash screen"""
    try:
        splash.showMessage("🔄 Verificando actualizaciones...", 
                          Qt.AlignCenter | Qt.AlignBottom, 
                          Qt.white)
        app.processEvents()
        
        from src.utils.updater import UpdateChecker
        
        checker = UpdateChecker(APP_VERSION, UPDATE_SERVER_URL)
        update_info = checker.check_for_updates()
        
        if update_info:
            splash.showMessage(f"🆕 Actualización disponible: v{update_info['version']}", 
                              Qt.AlignCenter | Qt.AlignBottom, 
                              Qt.yellow)
            app.processEvents()
            # Dar tiempo para que el usuario vea el mensaje
            QTimer.singleShot(2000, lambda: None)
        else:
            splash.showMessage("✅ Aplicación actualizada", 
                              Qt.AlignCenter | Qt.AlignBottom, 
                              Qt.green)
            app.processEvents()
            
    except Exception as e:
        print(f"⚠️ Error verificando actualizaciones: {e}")
        splash.showMessage("⚠️ No se pudo verificar actualizaciones", 
                          Qt.AlignCenter | Qt.AlignBottom, 
                          Qt.yellow)
        app.processEvents()


def load_components_async():
    """Cargar componentes de forma asíncrona después del splash"""
    # Importar solo cuando sea necesario
    from src.auth.login_manager import LoginManager
    from src.gui.main_window import MainWindow
    
    return LoginManager, MainWindow


def main():
    """Función principal optimizada para arranque ultra-rápido"""
    # Crear aplicación inmediatamente
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Configurar información de la aplicación
    app.setApplicationName("AlertasQB")
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("Monitoreo Geotécnico")
    
    # Mostrar splash screen inmediatamente (< 1 segundo)
    splash = create_splash_screen()
    splash.show()
    app.processEvents()  # Procesar eventos para mostrar splash
    
    # Cargar componentes de forma asíncrona
    splash.showMessage("📦 Cargando componentes...", 
                      Qt.AlignCenter | Qt.AlignBottom, 
                      Qt.white)
    app.processEvents()
    
    # Verificar actualizaciones durante la carga
    if UPDATE_CHECK_ON_STARTUP:
        check_updates_during_startup(splash, app)
    
    try:
        LoginManager, MainWindow = load_components_async()
        
        splash.showMessage("🔐 Preparando login...", 
                          Qt.AlignCenter | Qt.AlignBottom, 
                          Qt.white)
        app.processEvents()
        
        # Crear login manager
        login_manager = LoginManager()
        
        # Cerrar splash antes del login
        splash.finish(None)
        
        if login_manager.show_login():
            # Login exitoso - crear ventana principal
            main_window = MainWindow()
            main_window.set_current_user(login_manager.current_user)
            main_window.show()
            
            # Inicializar sistema de actualización después del login
            if UPDATE_CHECK_ON_STARTUP:
                initialize_updater(main_window, app)
            
            return app.exec()
        else:
            return 0
            
    except Exception as e:
        splash.showMessage(f"❌ Error: {str(e)}", 
                          Qt.AlignCenter | Qt.AlignBottom, 
                          Qt.red)
        app.processEvents()
        QTimer.singleShot(2000, app.quit)  # Cerrar después de 2 segundos
        return app.exec()


def initialize_updater(main_window, app):
    """Inicializar el sistema de actualización"""
    try:
        from src.utils.updater import AutoUpdater
        
        print(f"🔄 Inicializando sistema de actualización v{APP_VERSION}")
        
        updater = AutoUpdater(APP_VERSION, UPDATE_SERVER_URL, main_window)
        updater.check_for_updates_on_startup()
        
        print("✅ Sistema de actualización inicializado")
        
    except ImportError as e:
        print(f"⚠️ Sistema de actualización no disponible: {e}")
    except Exception as e:
        print(f"⚠️ Error al inicializar actualizador: {e}")


if __name__ == "__main__":
    sys.exit(main())
