"""
Configuración de versión de la aplicación
"""

# Versión actual de la aplicación (ACTUALIZAR CADA VEZ QUE HAGAS CAMBIOS)
APP_VERSION = "1.2.3"

# Servidor de actualizaciones (GitHub API para releases)
UPDATE_SERVER_URL = "https://api.github.com/repos/brunooviedo/AlertasQb/releases/latest"

# Configuraciones de actualización
UPDATE_CHECK_ON_STARTUP = True
UPDATE_CHECK_INTERVAL_HOURS = 24  # Verificar cada 24 horas
AUTO_DOWNLOAD = True  # Descargar automáticamente
FORCE_UPDATE = False  # Si True, fuerza la actualización sin opción de cancelar

# Información de la aplicación
APP_NAME = "AlertasQB"
APP_DESCRIPTION = "Sistema de Alertas Geotécnicas"
COMPANY_NAME = "Monitoreo Geotécnico"
COPYRIGHT = "© 2025 Bruno - Todos los derechos reservados"

# URLs útiles
GITHUB_REPO = "https://github.com/brunooviedo/AlertasQb"
SUPPORT_EMAIL = "bruno@alertasqb.com"
DOCUMENTATION_URL = "https://github.com/brunooviedo/AlertasQb/blob/main/README.md"
