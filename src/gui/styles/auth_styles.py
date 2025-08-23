#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E            QLabel[fieldLabel="true"] {
                color: white;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI';
                background-color: rgba(0, 0, 0, 0.4);
                padding: 10px 15px;
                border-radius: 6px;
                min-width: 300px;
            }ra el sistema de autenticación (Login y registro)
Desarrollado por Bruno Oviedo © 2025
"""

from .theme import AppTheme

class AuthStyles:
    """Estilos para ventanas de autenticación"""
    
    @staticmethod
    def get_login_dialog_styles():
        """Estilos para el diálogo de login mejorado"""
        return f"""
            QDialog {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {AppTheme.PRIMARY_BLUE},
                    stop: 1 #2d4dd1
                );
                border-radius: {AppTheme.BORDER_RADIUS};
            }}
            
            QLabel {{
                color: white;
                font-family: 'Segoe UI';
                border: none;
                background: transparent;
                font-size: 14px;
            }}
            
            QLabel[titleLabel="true"] {{
                color: white;
                font-size: 36px;
                font-weight: bold;
                font-family: 'Segoe UI';
                background-color: rgba(0, 0, 0, 0.3);
                padding: 20px 40px;
                border-radius: 15px;
                min-height: 80px;
            }}
            
            QLabel[subtitleLabel="true"] {{
                color: white;
                font-size: 18px;
                font-family: 'Segoe UI';
                font-weight: normal;
                background-color: rgba(0, 0, 0, 0.2);
                padding: 10px 20px;
                border-radius: 8px;
                min-height: 40px;
            }}
            
            QLabel[fieldLabel="true"] {{
                color: white;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI';
                background-color: rgba(0, 0, 0, 0.4);
                padding: 8px 15px;
                border-radius: 6px;
            }}
        """
    
    @staticmethod
    def get_input_styles():
        """Estilos para campos de entrada mejorados"""
        return f"""
            QLineEdit {{
                background-color: rgba(255, 255, 255, 0.95);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 15px 20px;
                font-size: 14px;
                font-family: {AppTheme.FONT_FAMILY};
                color: #333333;
                selection-background-color: {AppTheme.PRIMARY_BLUE};
                min-height: 20px;
            }}
            
            QLineEdit:focus {{
                border-color: {AppTheme.WHITE};
                background-color: {AppTheme.WHITE};
            }}
            
            QLineEdit:hover {{
                border-color: rgba(255, 255, 255, 0.5);
            }}
            
            QLineEdit::placeholder {{
                color: #888888;
                font-style: italic;
            }}
        """
    
    @staticmethod
    def get_button_styles():
        """Estilos para botones de autenticación mejorados"""
        return f"""
            QPushButton[loginButton="true"] {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(255, 255, 255, 0.95),
                    stop: 1 rgba(255, 255, 255, 0.85)
                );
                color: {AppTheme.PRIMARY_BLUE};
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                font-family: {AppTheme.FONT_FAMILY};
                min-width: 140px;
            }}
            
            QPushButton[loginButton="true"]:hover {{
                background: {AppTheme.WHITE};
                border-color: {AppTheme.WHITE};
            }}
            
            QPushButton[loginButton="true"]:pressed {{
                background: rgba(255, 255, 255, 0.7);
            }}
            
            QPushButton[cancelButton="true"] {{
                background: rgba(255, 255, 255, 0.1);
                color: {AppTheme.WHITE};
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                font-family: {AppTheme.FONT_FAMILY};
                min-width: 140px;
            }}
            
            QPushButton[cancelButton="true"]:hover {{
                background: rgba(255, 255, 255, 0.2);
                border-color: {AppTheme.WHITE};
            }}
            
            QPushButton[createButton="true"], QPushButton[changePasswordButton="true"] {{
                background: rgba(255, 255, 255, 0.1);
                color: {AppTheme.WHITE};
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
                font-family: {AppTheme.FONT_FAMILY};
                min-width: 120px;
            }}
            
            QPushButton[createButton="true"]:hover, QPushButton[changePasswordButton="true"]:hover {{
                background: rgba(255, 255, 255, 0.15);
                border-color: rgba(255, 255, 255, 0.4);
            }}
        """
    
    @staticmethod
    def get_info_styles():
        """Estilos para etiquetas informativas"""
        return f"""
            QLabel[infoLabel="true"] {{
                color: {AppTheme.WHITE};
                font-size: 13px;
                font-weight: bold;
                margin-top: 20px;
                text-align: center;
                font-family: {AppTheme.FONT_FAMILY};
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 8px;
                padding: 12px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
        """
    
    @staticmethod
    def get_registration_dialog_styles():
        """Estilos para el diálogo de registro con paleta Teck"""
        return f"""
            QDialog {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {AppTheme.TECK_GREEN},
                    stop: 1 {AppTheme.TECK_GREEN_LIGHT}
                );
                border-radius: {AppTheme.BORDER_RADIUS};
            }}
            
            QLabel {{
                color: {AppTheme.WHITE};
                font-family: {AppTheme.FONT_FAMILY};
                border: none;
                background: transparent;
            }}
            
            QLabel[registrationTitle="true"] {{
                color: {AppTheme.WHITE};
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 15px;
                text-align: center;
                font-family: {AppTheme.FONT_FAMILY};
            }}
            
            QLabel[registrationField="true"] {{
                color: {AppTheme.WHITE};
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-weight: 600;
                margin-bottom: 6px;
                font-family: {AppTheme.FONT_FAMILY};
            }}
            
            QPushButton[registerButton="true"] {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {AppTheme.TECK_GREEN},
                    stop: 1 #008554
                );
                color: {AppTheme.WHITE};
                border: none;
                border-radius: {AppTheme.BORDER_RADIUS};
                padding: 15px 25px;
                font-size: 16px;
                font-weight: bold;
                font-family: {AppTheme.FONT_FAMILY};
                min-width: 120px;
            }}
            
            QPushButton[registerButton="true"]:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #008554,
                    stop: 1 #006640
                );
            }}
            
            QPushButton[registerCancelButton="true"] {{
                background-color: {AppTheme.TECK_GRAY};
                color: {AppTheme.WHITE};
                border: none;
                border-radius: {AppTheme.BORDER_RADIUS};
                padding: 15px 25px;
                font-size: 16px;
                font-weight: bold;
                font-family: {AppTheme.FONT_FAMILY};
                min-width: 120px;
            }}
            
            QPushButton[registerCancelButton="true"]:hover {{
                background-color: #3f5a73;
            }}
        """
    
    @staticmethod
    def get_change_password_dialog_styles():
        """Estilos para el diálogo de cambio de contraseña con paleta Teck"""
        return f"""
            QDialog {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {AppTheme.TECK_COPPER},
                    stop: 1 #ff7f26
                );
                border-radius: {AppTheme.BORDER_RADIUS};
            }}
            
            QLabel {{
                color: {AppTheme.WHITE};
                font-family: {AppTheme.FONT_FAMILY};
                border: none;
                background: transparent;
            }}
            
            QLabel[changePasswordTitle="true"] {{
                color: {AppTheme.WHITE};
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 15px;
                text-align: center;
                font-family: {AppTheme.FONT_FAMILY};
            }}
            
            QLabel[changePasswordField="true"] {{
                color: {AppTheme.WHITE};
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-weight: 600;
                margin-bottom: 6px;
                font-family: {AppTheme.FONT_FAMILY};
            }}
            
            QPushButton[changePasswordButton="true"] {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {AppTheme.TECK_COPPER},
                    stop: 1 #e6732a
                );
                color: {AppTheme.WHITE};
                border: none;
                border-radius: {AppTheme.BORDER_RADIUS};
                padding: 15px 25px;
                font-size: 16px;
                font-weight: bold;
                font-family: {AppTheme.FONT_FAMILY};
                min-width: 120px;
            }}
            
            QPushButton[changePasswordButton="true"]:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #e6732a,
                    stop: 1 #cc5f1e
                );
            }}
        """
    
    @staticmethod
    def get_complete_auth_styles():
        """Retorna todos los estilos de autenticación combinados"""
        return f"""
            {AuthStyles.get_login_dialog_styles()}
            {AuthStyles.get_input_styles()}
            {AuthStyles.get_button_styles()}
            {AuthStyles.get_info_styles()}
        """
