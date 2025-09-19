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
    splash.setFixedSize(450, 220)
    
    # Configurar apariencia moderna con gradiente
    splash.setStyleSheet("""
        QSplashScreen {
            background: qlineargradient(
                x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #3153E4,
                stop: 1 #1a237e
            );
            border: 2px solid #00A26A;
            border-radius: 15px;
            color: white;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
            font-weight: bold;
        }
    """)
    
    # Agregar texto con mejor contraste
    splash.showMessage("📱 AlertasQB - Cargando...", 
                      Qt.AlignCenter | Qt.AlignBottom, 
                      Qt.white)
    
    return splash


def show_splash_message(splash, app, message, color=Qt.white, delay=0):
    """Mostrar mensaje en splash con color y delay opcional"""
    splash.showMessage(message, 
                      Qt.AlignCenter | Qt.AlignBottom, 
                      color)
    app.processEvents()
    if delay > 0:
        import time
        time.sleep(delay)


def check_updates_during_startup(splash, app):
    """Verificar actualizaciones durante el splash screen"""
    try:
        # Mensaje inicial con color blanco brillante
        show_splash_message(splash, app, "🔄 Verificando actualizaciones...", Qt.white)
        
        from src.utils.updater import UpdateChecker
        
        checker = UpdateChecker(APP_VERSION, UPDATE_SERVER_URL)
        update_info = checker.check_for_updates()
        
        if update_info:
            # Amarillo brillante para actualizaciones disponibles
            show_splash_message(splash, app, 
                              f"🆕 Actualización disponible: v{update_info['version']}", 
                              Qt.GlobalColor.yellow, 2.5)
        else:
            # Verde brillante para confirmación
            show_splash_message(splash, app, 
                              "✅ Aplicación actualizada", 
                              Qt.GlobalColor.green, 1.5)
            
    except Exception as e:
        print(f"⚠️ Error verificando actualizaciones: {e}")
        # Cyan brillante para advertencias (mejor contraste)
        show_splash_message(splash, app, 
                          "⚠️ No se pudo verificar actualizaciones", 
                          Qt.GlobalColor.cyan, 1.5)


def load_components_async():
    """Cargar componentes de forma asíncrona después del splash"""
    # Importar solo cuando sea necesario
    from src.auth.login_manager import LoginManager
    from src.gui.main_window import MainWindow
    
    return LoginManager, MainWindow


def preload_heavy_libraries(splash, app):
    """Precargar librerías pesadas durante el splash screen"""
    try:
        # 1. Matplotlib (la más pesada - ~1-2 segundos)
        show_splash_message(splash, app, "📊 Cargando matplotlib...", Qt.white)
        import matplotlib
        matplotlib.use('Agg', force=True)  # Configurar backend
        import matplotlib.pyplot as plt
        plt.ioff()  # Desactivar modo interactivo
        
        # 2. Pandas (muy pesada - ~0.5-1 segundo)  
        show_splash_message(splash, app, "📋 Cargando pandas...", Qt.white)
        import pandas as pd
        
        # 3. Numpy (moderada - ~0.2-0.5 segundos)
        show_splash_message(splash, app, "🔢 Cargando numpy...", Qt.white)
        import numpy as np
        
        # 4. OpenPyXL (moderada - ~0.1-0.3 segundos)
        show_splash_message(splash, app, "📄 Cargando openpyxl...", Qt.white)
        import openpyxl
        
        # 5. Seaborn (opcional pero pesada si se usa)
        try:
            show_splash_message(splash, app, "🎨 Cargando seaborn...", Qt.white)
            import seaborn as sns
        except ImportError:
            pass  # No es crítica
            
        show_splash_message(splash, app, "✅ Librerías cargadas exitosamente", Qt.GlobalColor.green, 0.5)
        
    except Exception as e:
        print(f"⚠️ Error precargando librerías: {e}")
        show_splash_message(splash, app, 
                          "⚠️ Error cargando algunas librerías", 
                          Qt.GlobalColor.yellow, 1)


def preload_heavy_widgets(splash, app):
    """Precargar widgets pesados que usan las librerías ya cargadas"""
    try:
        # 1. Dashboard (usa matplotlib + pandas + numpy)
        show_splash_message(splash, app, "🎯 Preparando dashboard...", Qt.white)
        from src.gui.dashboard import Dashboard
        # No instanciar aún, solo cargar el módulo
        
        # 2. Data Manager (usa pandas + openpyxl)
        show_splash_message(splash, app, "🗄️ Preparando gestión de datos...", Qt.white)  
        from src.gui.data_manager_new import DataManagerWidget
        
        # 3. Alerts Viewer (usa pandas)
        show_splash_message(splash, app, "📊 Preparando visualizador de alertas...", Qt.white)
        from src.gui.alerts_data_viewer import AlertsDataViewer
        
        # 4. Alert Form (usa openpyxl)
        show_splash_message(splash, app, "📝 Preparando formulario de alertas...", Qt.white)
        from src.gui.alert_form import AlertForm
        
        show_splash_message(splash, app, "🚀 Widgets preparados exitosamente", Qt.GlobalColor.green, 0.5)
        
    except Exception as e:
        print(f"⚠️ Error precargando widgets: {e}")
        show_splash_message(splash, app, 
                          "⚠️ Error preparando algunos componentes", 
                          Qt.GlobalColor.yellow, 1)


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
    show_splash_message(splash, app, "📦 Cargando componentes...", Qt.white)
    
    # Precargar librerías pesadas durante el splash
    preload_heavy_libraries(splash, app)
    
    # Precargar widgets pesados que usan las librerías
    preload_heavy_widgets(splash, app)
    
    # Verificar actualizaciones durante la carga
    if UPDATE_CHECK_ON_STARTUP:
        check_updates_during_startup(splash, app)
    
    try:
        LoginManager, MainWindow = load_components_async()
        
        show_splash_message(splash, app, "🔐 Preparando sistema de login...", Qt.white)
        
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
        # Mensaje de error en rojo brillante con alta visibilidad
        show_splash_message(splash, app, 
                          f"❌ Error de inicio: {str(e)[:50]}...", 
                          Qt.GlobalColor.red, 3)
        return app.exec()


def initialize_updater(main_window, app):
    """Inicializar el sistema de actualización"""
    try:
        from src.utils.updater import AutoUpdater
        
        print(f"🔄 Inicializando sistema de actualización v{APP_VERSION}")
        
        updater = AutoUpdater(UPDATE_SERVER_URL, APP_VERSION, main_window)
        updater.check_for_updates_on_startup()
        
        print("✅ Sistema de actualización inicializado")
        
    except ImportError as e:
        print(f"⚠️ Sistema de actualización no disponible: {e}")
    except Exception as e:
        print(f"⚠️ Error al inicializar actualizador: {e}")


if __name__ == "__main__":
    sys.exit(main())
