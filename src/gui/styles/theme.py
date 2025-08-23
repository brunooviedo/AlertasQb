#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paleta de colores y variables globales para el Sistema de Alertas Geotécnicas
Desarrollado por Bruno Oviedo © 2025
"""

class AppTheme:
    """Paleta de colores corporativos Teck y configuración de tema global"""
    
    # ==================== COLORES CORPORATIVOS TECK ====================
    # Azul Medio - Color principal
    PRIMARY_BLUE = "#3153E4"       # PMS 2728C - CMYK: 90/60/0/0
    TECK_BLUE_MEDIUM = "#3153E4"   # RGB: 49/83/228
    
    # Cobre - Color secundario principal
    TECK_COPPER = "#FF9040"        # PMS 1495C - CMYK: 0/53/95/0 - RGB: 255/144/64
    TECK_COPPER_DARK = "#C7420B"   # PMS 173C - CMYK: 0/85/94/3 - RGB: 199/66/11
    
    # Azul Claro - Para fondos y elementos suaves
    TECK_BLUE_LIGHT = "#AAE5E3"    # PMS 635C - CMYK: 34/1/7/0 - RGB: 170/229/227
    
    # Grises y neutros
    TECK_GRAY = "#51728E"          # PMS 5405C - CMYK: 48/20/0/34 - RGB: 81/114/142
    
    # Morado - Para elementos especiales
    TECK_PURPLE = "#46195E"        # PMS 2607C - CMYK: 82/100/0/4 - RGB: 70/25/94
    
    # Verdes - Para éxito y confirmaciones
    TECK_GREEN_LIGHT = "#00DBB7"   # PMS 333C - CMYK: 62/0/35/0 - RGB: 0/219/183
    TECK_GREEN = "#00A26A"         # PMS 7724C - CMYK: 85/0/75/0 - RGB: 0/162/106
    
    # ==================== MAPEO DE COLORES FUNCIONALES ====================
    # Colores principales basados en Teck
    PRIMARY_GREEN = TECK_GREEN
    PRIMARY_RED = TECK_COPPER_DARK
    PRIMARY_YELLOW = TECK_COPPER
    PRIMARY_ORANGE = TECK_COPPER
    
    # Colores de estado usando paleta Teck
    SUCCESS = TECK_GREEN
    WARNING = TECK_COPPER
    ERROR = TECK_COPPER_DARK
    INFO = TECK_BLUE_LIGHT
    
    # Colores neutros
    WHITE = "#ffffff"
    LIGHT_GRAY = "#f8f9fa"
    MEDIUM_GRAY = "#e9ecef"
    BORDER_GRAY = "#dee2e6"
    TEXT_GRAY = TECK_GRAY
    DARK_GRAY = "#6c757d"
    BLACK = "#212529"
    
    # Colores específicos de alertas usando paleta Teck
    ALERT_GREEN = "#e8f5f2"        # Verde claro derivado
    ALERT_YELLOW = "#fff5e6"       # Cobre claro derivado  
    ALERT_RED = "#fdeaea"          # Cobre oscuro claro derivado
    
    # Tipografía
    FONT_FAMILY = "'Segoe UI', 'Arial', sans-serif"
    FONT_SIZE_SMALL = "12px"
    FONT_SIZE_NORMAL = "14px"
    FONT_SIZE_LARGE = "18px"
    FONT_SIZE_TITLE = "24px"
    
    # Espaciado
    PADDING_SMALL = "8px"
    PADDING_NORMAL = "12px"
    PADDING_LARGE = "20px"
    
    # Bordes
    BORDER_RADIUS = "8px"
    BORDER_RADIUS_SMALL = "4px"
    BORDER_WIDTH = "1px"
