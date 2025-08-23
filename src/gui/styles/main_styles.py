#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estilos CSS centralizados para el Sistema de Alertas Geotécnicas
Desarrollado por Bruno Oviedo © 2025
"""

from .theme import AppTheme
from .auth_styles import AuthStyles
from .form_styles import FormStyles
from .dialog_styles import DialogStyles
from .table_styles import TableStyles

class MainWindowStyles:
    """Clase que contiene todos los estilos CSS para la ventana principal"""
    
    @staticmethod
    def get_main_styles():
        """Retorna los estilos principales de la aplicación"""
        return f"""
            QMainWindow {{
                background-color: {AppTheme.WHITE};
                color: {AppTheme.BLACK};
                font-family: {AppTheme.FONT_FAMILY};
            }}
            
            QFrame {{
                background-color: {AppTheme.WHITE};
                border: 1px solid {AppTheme.BORDER_GRAY};
                border-radius: {AppTheme.BORDER_RADIUS};
                color: {AppTheme.BLACK};
            }}
            
            QStatusBar {{
                background-color: #343a40;
                color: {AppTheme.WHITE};
                border: none;
                font-weight: 500;
                padding: 5px 10px;
                font-family: {AppTheme.FONT_FAMILY};
            }}
            
            QMenuBar {{
                background-color: {AppTheme.LIGHT_GRAY};
                color: {AppTheme.BLACK};
                border-bottom: 1px solid {AppTheme.BORDER_GRAY};
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-family: {AppTheme.FONT_FAMILY};
            }}
            
            QMenuBar::item {{
                background-color: transparent;
                padding: 8px 12px;
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
            }}
            
            QMenuBar::item:selected {{
                background-color: {AppTheme.MEDIUM_GRAY};
                color: {AppTheme.BLACK};
            }}
            
            QMenu {{
                background-color: {AppTheme.WHITE};
                color: {AppTheme.BLACK};
                border: 1px solid {AppTheme.BORDER_GRAY};
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                padding: 5px;
                font-family: {AppTheme.FONT_FAMILY};
            }}
            
            QMenu::item {{
                padding: 8px 20px;
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
            }}
            
            QMenu::item:selected {{
                background-color: {AppTheme.PRIMARY_BLUE};
                color: {AppTheme.WHITE};
            }}
        """
    
    @staticmethod
    def get_header_styles():
        """Retorna estilos específicos para el header"""
        return f"""
            QLabel {{
                color: {AppTheme.BLACK};
                font-family: {AppTheme.FONT_FAMILY};
            }}
            
            QLabel[headerTitle="true"] {{
                font-size: {AppTheme.FONT_SIZE_TITLE};
                font-weight: 700;
                color: {AppTheme.PRIMARY_BLUE};
                margin-bottom: 5px;
            }}
            
            QLabel[userInfo="true"] {{
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-weight: 600;
                color: {AppTheme.TEXT_GRAY};
                text-align: right;
            }}
            
            QLabel[datetime="true"] {{
                font-size: {AppTheme.FONT_SIZE_SMALL};
                color: {AppTheme.DARK_GRAY};
                text-align: right;
            }}
        """
    
    @staticmethod
    def get_tab_styles():
        """Retorna estilos específicos para las pestañas"""
        return f"""
            QTabWidget::pane {{
                border: 1px solid {AppTheme.BORDER_GRAY};
                border-radius: {AppTheme.BORDER_RADIUS};
                background-color: {AppTheme.WHITE};
                margin-top: 5px;
            }}
            
            QTabWidget::tab-bar {{
                alignment: left;
            }}
            
            QTabBar::tab {{
                background-color: {AppTheme.LIGHT_GRAY};
                color: {AppTheme.TEXT_GRAY};
                border: 2px solid {AppTheme.BORDER_GRAY};
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: {AppTheme.BORDER_RADIUS};
                border-top-right-radius: {AppTheme.BORDER_RADIUS};
                font-weight: 500;
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-family: {AppTheme.FONT_FAMILY};
                min-width: 120px;
            }}
            
            QTabBar::tab:selected {{
                background-color: {AppTheme.WHITE};
                color: {AppTheme.BLACK};
                border-bottom-color: {AppTheme.WHITE};
                font-weight: 600;
            }}
            
            QTabBar::tab:hover {{
                background-color: {AppTheme.MEDIUM_GRAY};
                color: {AppTheme.TEXT_GRAY};
            }}
        """
    
    @staticmethod
    def get_complete_styles():
        """Retorna todos los estilos combinados"""
        return f"""
            {MainWindowStyles.get_main_styles()}
            {MainWindowStyles.get_header_styles()}
            {MainWindowStyles.get_tab_styles()}
        """

# Clase de acceso unificado a todos los estilos
class AppStyles:
    """Clase unificada para acceso a todos los estilos de la aplicación"""
    
    @staticmethod
    def get_main_window_styles():
        """Estilos para la ventana principal"""
        return MainWindowStyles.get_complete_styles()
    
    @staticmethod
    def get_auth_styles():
        """Estilos para autenticación"""
        return AuthStyles.get_complete_auth_styles()
    
    @staticmethod
    def get_form_styles():
        """Estilos para formularios"""
        return FormStyles.get_complete_form_styles()
    
    @staticmethod
    def get_dialog_styles():
        """Estilos para diálogos"""
        return DialogStyles.get_complete_dialog_styles()
    
    @staticmethod
    def get_table_styles():
        """Estilos para tablas"""
        return TableStyles.get_complete_table_styles()
    
    @staticmethod
    def get_all_styles():
        """Todos los estilos de la aplicación combinados"""
        return f"""
            {AppStyles.get_main_window_styles()}
            {AppStyles.get_form_styles()}
            {AppStyles.get_dialog_styles()}
            {AppStyles.get_table_styles()}
        """
