#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estilos para formularios de la aplicación
Desarrollado por Bruno Oviedo © 2025
"""

from .theme import AppTheme

class FormStyles:
    """Estilos para formularios y componentes de entrada de datos"""
    
    @staticmethod
    def get_form_container_styles():
        """Estilos para contenedores de formularios"""
        return f"""
            QWidget {{
                background-color: {AppTheme.WHITE};
                font-family: {AppTheme.FONT_FAMILY};
            }}
            
            QGroupBox {{
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-weight: bold;
                color: {AppTheme.BLACK};
                border: 1px solid {AppTheme.BORDER_GRAY};
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                margin-top: 8px;
                margin-bottom: 8px;
                padding-top: 12px;
                padding-bottom: 8px;
                font-family: {AppTheme.FONT_FAMILY};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 5px 0 5px;
                color: {AppTheme.PRIMARY_BLUE};
                font-weight: bold;
                font-size: {AppTheme.FONT_SIZE_NORMAL};
            }}
        """
    
    @staticmethod
    def get_form_input_styles():
        """Estilos para campos de entrada de formularios"""
        return f"""
            QLineEdit, QDateEdit, QTimeEdit, QDateTimeEdit {{
                background-color: {AppTheme.WHITE};
                border: 1px solid {AppTheme.BORDER_GRAY};
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                padding: 4px 8px;
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-family: {AppTheme.FONT_FAMILY};
                color: {AppTheme.BLACK};
                selection-background-color: {AppTheme.PRIMARY_BLUE};
                min-height: 14px;
                max-height: 24px;
            }}
            
            QTextEdit {{
                background-color: {AppTheme.WHITE};
                border: 1px solid {AppTheme.BORDER_GRAY};
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                padding: 6px 8px;
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-family: {AppTheme.FONT_FAMILY};
                color: {AppTheme.BLACK};
                selection-background-color: {AppTheme.PRIMARY_BLUE};
                min-height: 60px;
            }}
            
            QLineEdit:focus, QTextEdit:focus, QDateEdit:focus, 
            QTimeEdit:focus, QDateTimeEdit:focus {{
                border-color: {AppTheme.PRIMARY_BLUE};
            }}
            
            QLineEdit:hover, QTextEdit:hover, QDateEdit:hover,
            QTimeEdit:hover, QDateTimeEdit:hover {{
                border-color: #80bdff;
                background-color: #f8f9fa;
            }}
            
            QComboBox {{
                background-color: {AppTheme.WHITE};
                border: 1px solid {AppTheme.BORDER_GRAY};
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                padding: 4px 8px;
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-family: {AppTheme.FONT_FAMILY};
                color: {AppTheme.BLACK};
                min-height: 14px;
                max-height: 24px;
                padding-right: 20px;
            }}
            
            QComboBox:focus {{
                border-color: {AppTheme.PRIMARY_BLUE};
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 16px;
                right: 2px;
            }}
            
            QComboBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid {AppTheme.TEXT_GRAY};
                margin-right: 6px;
            }}
            
            QComboBox QAbstractItemView {{
                border: 1px solid {AppTheme.BORDER_GRAY};
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                background-color: {AppTheme.WHITE};
                selection-background-color: {AppTheme.PRIMARY_BLUE};
                color: {AppTheme.BLACK};
            }}
        """
    
    @staticmethod
    def get_form_button_styles():
        """Estilos para botones de formularios con colores corporativos Teck"""
        return f"""
            QPushButton {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {AppTheme.PRIMARY_BLUE},
                    stop: 1 #2944cc
                );
                color: {AppTheme.WHITE};
                border: none;
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                padding: 8px 20px;
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-weight: bold;
                font-family: {AppTheme.FONT_FAMILY};
                min-height: 20px;
            }}
            
            QPushButton:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2944cc,
                    stop: 1 #1e35b5
                );
            }}
            
            QPushButton:pressed {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #1e35b5,
                    stop: 1 #152899
                );
            }}
            
            QPushButton:disabled {{
                background-color: {AppTheme.BORDER_GRAY};
                color: {AppTheme.DARK_GRAY};
            }}
            
            QPushButton[saveButton="true"] {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {AppTheme.TECK_GREEN},
                    stop: 1 #008554
                );
            }}
            
            QPushButton[saveButton="true"]:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #008554,
                    stop: 1 #006640
                );
            }}
            
            QPushButton[clearButton="true"] {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {AppTheme.TECK_COPPER},
                    stop: 1 #e67f2e
                );
            }}
            
            QPushButton[clearButton="true"]:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #e67f2e,
                    stop: 1 {AppTheme.TECK_COPPER_DARK}
                );
            }}
        """
    
    @staticmethod
    def get_form_label_styles():
        """Estilos para etiquetas de formularios"""
        return f"""
            QLabel {{
                color: {AppTheme.BLACK};
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-family: {AppTheme.FONT_FAMILY};
                margin-bottom: 2px;
                padding: 2px 0px;
            }}
            
            QLabel[fieldLabel="true"] {{
                font-weight: 600;
                color: {AppTheme.TEXT_GRAY};
                margin-bottom: 4px;
                padding: 2px 0px;
            }}
            
            QLabel[titleLabel="true"] {{
                font-size: {AppTheme.FONT_SIZE_LARGE};
                font-weight: bold;
                color: {AppTheme.PRIMARY_BLUE};
                margin-bottom: 15px;
                padding: 8px 0px;
                text-align: center;
            }}
            
            QLabel[errorLabel="true"] {{
                color: {AppTheme.ERROR};
                font-size: {AppTheme.FONT_SIZE_SMALL};
                font-style: italic;
                margin-top: 5px;
            }}
            
            QLabel[successLabel="true"] {{
                color: {AppTheme.SUCCESS};
                font-size: {AppTheme.FONT_SIZE_SMALL};
                font-weight: 600;
                margin-top: 10px;
            }}
        """
    
    @staticmethod
    def get_complete_form_styles():
        """Retorna todos los estilos de formularios combinados"""
        return f"""
            {FormStyles.get_form_container_styles()}
            {FormStyles.get_form_input_styles()}
            {FormStyles.get_form_button_styles()}
            {FormStyles.get_form_label_styles()}
        """
