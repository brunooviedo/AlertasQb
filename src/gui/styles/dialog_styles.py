#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estilos para diálogos y ventanas modales
Desarrollado por Bruno Oviedo © 2025
"""

from .theme import AppTheme

class DialogStyles:
    """Estilos para diálogos y ventanas modales"""
    
    @staticmethod
    def get_dialog_container_styles():
        """Estilos para contenedores de diálogos"""
        return f"""
            QDialog {{
                background-color: {AppTheme.WHITE};
                border-radius: {AppTheme.BORDER_RADIUS};
                border: 2px solid {AppTheme.BORDER_GRAY};
                font-family: {AppTheme.FONT_FAMILY};
            }}
            
            QDialog QWidget {{
                background-color: transparent;
            }}
        """
    
    @staticmethod
    def get_about_dialog_styles():
        """Estilos específicos para el diálogo Acerca de"""
        return f"""
            QLabel[aboutTitle="true"] {{
                color: #2c3e50;
                font-size: {AppTheme.FONT_SIZE_TITLE};
                font-weight: bold;
                margin-bottom: 10px;
                text-align: center;
                font-family: {AppTheme.FONT_FAMILY};
            }}
            
            QLabel[aboutVersion="true"] {{
                color: #7f8c8d;
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                margin-bottom: 15px;
                text-align: center;
                font-family: {AppTheme.FONT_FAMILY};
            }}
            
            QTextEdit[aboutInfo="true"] {{
                background-color: #f8f9fa;
                border: 1px solid {AppTheme.BORDER_GRAY};
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                padding: 15px;
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-family: {AppTheme.FONT_FAMILY};
                color: #2c3e50;
                selection-background-color: {AppTheme.PRIMARY_BLUE};
            }}
            
            QLabel[aboutDeveloper="true"] {{
                color: {AppTheme.PRIMARY_BLUE};
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                margin: 15px 0px;
                font-family: {AppTheme.FONT_FAMILY};
                padding: 10px;
                background-color: #e3f2fd;
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                border: 1px solid #90caf9;
            }}
            
            QPushButton[aboutClose="true"] {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {AppTheme.PRIMARY_BLUE},
                    stop: 1 #0056b3
                );
                color: {AppTheme.WHITE};
                border: none;
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                padding: 12px 30px;
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-weight: bold;
                font-family: {AppTheme.FONT_FAMILY};
                min-width: 100px;
            }}
            
            QPushButton[aboutClose="true"]:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #0056b3,
                    stop: 1 #004085
                );
            }}
        """
    
    @staticmethod
    def get_settings_dialog_styles():
        """Estilos para el diálogo de configuración"""
        return f"""
            QTabWidget {{
                border: none;
                background-color: {AppTheme.WHITE};
            }}
            
            QTabWidget::pane {{
                border: 1px solid {AppTheme.BORDER_GRAY};
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                background-color: {AppTheme.WHITE};
                margin-top: 5px;
            }}
            
            QTabBar::tab {{
                background-color: {AppTheme.LIGHT_GRAY};
                color: {AppTheme.TEXT_GRAY};
                border: 1px solid {AppTheme.BORDER_GRAY};
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: {AppTheme.BORDER_RADIUS_SMALL};
                border-top-right-radius: {AppTheme.BORDER_RADIUS_SMALL};
                font-family: {AppTheme.FONT_FAMILY};
                font-weight: 500;
            }}
            
            QTabBar::tab:selected {{
                background-color: {AppTheme.WHITE};
                color: {AppTheme.BLACK};
                border-bottom-color: {AppTheme.WHITE};
                font-weight: bold;
            }}
            
            QTabBar::tab:hover {{
                background-color: {AppTheme.MEDIUM_GRAY};
            }}
        """
    
    @staticmethod
    def get_user_management_styles():
        """Estilos para el diálogo de gestión de usuarios"""
        return f"""
            QTableWidget {{
                background-color: {AppTheme.WHITE};
                border: 1px solid {AppTheme.BORDER_GRAY};
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                gridline-color: {AppTheme.MEDIUM_GRAY};
                font-family: {AppTheme.FONT_FAMILY};
                selection-background-color: {AppTheme.PRIMARY_BLUE};
                selection-color: {AppTheme.WHITE};
            }}
            
            QTableWidget::item {{
                padding: {AppTheme.PADDING_SMALL};
                border-bottom: 1px solid {AppTheme.MEDIUM_GRAY};
            }}
            
            QTableWidget::item:selected {{
                background-color: {AppTheme.PRIMARY_BLUE};
                color: {AppTheme.WHITE};
            }}
            
            QHeaderView::section {{
                background-color: {AppTheme.LIGHT_GRAY};
                color: {AppTheme.BLACK};
                border: 1px solid {AppTheme.BORDER_GRAY};
                padding: 8px;
                font-weight: bold;
                font-family: {AppTheme.FONT_FAMILY};
            }}
            
            QPushButton[userManagement="true"] {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {AppTheme.SUCCESS},
                    stop: 1 #1e7e34
                );
                color: {AppTheme.WHITE};
                border: none;
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                padding: 10px 20px;
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-weight: bold;
                font-family: {AppTheme.FONT_FAMILY};
                margin: 5px;
            }}
            
            QPushButton[userManagement="true"]:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #1e7e34,
                    stop: 1 #155724
                );
            }}
            
            QPushButton[refreshButton="true"] {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {AppTheme.INFO},
                    stop: 1 #117a8b
                );
                color: {AppTheme.WHITE};
                border: none;
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                padding: 10px 20px;
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-weight: bold;
                font-family: {AppTheme.FONT_FAMILY};
                margin: 5px;
            }}
            
            QPushButton[refreshButton="true"]:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #117a8b,
                    stop: 1 #0c5460
                );
            }}
            
            QLabel[userStats="true"] {{
                color: #2E8B57;
                font-weight: bold;
                padding: 10px;
                font-family: {AppTheme.FONT_FAMILY};
                background-color: #f0f8f0;
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                border: 1px solid #90ee90;
            }}
        """
    
    @staticmethod
    def get_complete_dialog_styles():
        """Retorna todos los estilos de diálogos combinados"""
        return f"""
            {DialogStyles.get_dialog_container_styles()}
            {DialogStyles.get_about_dialog_styles()}
            {DialogStyles.get_settings_dialog_styles()}
            {DialogStyles.get_user_management_styles()}
        """
