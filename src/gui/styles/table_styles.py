#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estilos para tablas y visualización de datos
Desarrollado por Bruno Oviedo © 2025
"""

from .theme import AppTheme

class TableStyles:
    """Estilos para tablas y componentes de datos"""
    
    @staticmethod
    def get_data_table_styles():
        """Estilos para tablas de datos"""
        return f"""
            QTableWidget {{
                background-color: {AppTheme.WHITE};
                border: 1px solid {AppTheme.BORDER_GRAY};
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                gridline-color: {AppTheme.MEDIUM_GRAY};
                font-family: {AppTheme.FONT_FAMILY};
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                selection-background-color: {AppTheme.PRIMARY_BLUE};
                selection-color: {AppTheme.WHITE};
                alternate-background-color: #f8f9fa;
            }}
            
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {AppTheme.MEDIUM_GRAY};
                color: {AppTheme.BLACK};
            }}
            
            QTableWidget::item:selected {{
                background-color: {AppTheme.PRIMARY_BLUE};
                color: {AppTheme.WHITE};
            }}
            
            QTableWidget::item:hover {{
                background-color: #e9ecef;
            }}
            
            QHeaderView::section {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {AppTheme.LIGHT_GRAY},
                    stop: 1 {AppTheme.MEDIUM_GRAY}
                );
                color: {AppTheme.BLACK};
                border: 1px solid {AppTheme.BORDER_GRAY};
                padding: 10px 8px;
                font-weight: bold;
                font-family: {AppTheme.FONT_FAMILY};
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                text-align: left;
            }}
            
            QHeaderView::section:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {AppTheme.MEDIUM_GRAY},
                    stop: 1 {AppTheme.BORDER_GRAY}
                );
            }}
            
            QScrollBar:vertical {{
                border: 1px solid {AppTheme.BORDER_GRAY};
                background-color: {AppTheme.LIGHT_GRAY};
                width: 16px;
                border-radius: 8px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {AppTheme.TEXT_GRAY};
                border-radius: 6px;
                min-height: 20px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {AppTheme.DARK_GRAY};
            }}
            
            QScrollBar:horizontal {{
                border: 1px solid {AppTheme.BORDER_GRAY};
                background-color: {AppTheme.LIGHT_GRAY};
                height: 16px;
                border-radius: 8px;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: {AppTheme.TEXT_GRAY};
                border-radius: 6px;
                min-width: 20px;
                margin: 2px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background-color: {AppTheme.DARK_GRAY};
            }}
        """
    
    @staticmethod
    def get_filter_styles():
        """Estilos para controles de filtrado"""
        return f"""
            QWidget[filterContainer="true"] {{
                background-color: {AppTheme.LIGHT_GRAY};
                border: 1px solid {AppTheme.BORDER_GRAY};
                border-radius: {AppTheme.BORDER_RADIUS};
                padding: 15px;
                margin: 10px 0px;
            }}
            
            QLabel[filterLabel="true"] {{
                color: {AppTheme.BLACK};
                font-weight: bold;
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-family: {AppTheme.FONT_FAMILY};
                margin-bottom: 5px;
            }}
            
            QPushButton[filterButton="true"] {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {AppTheme.INFO},
                    stop: 1 #117a8b
                );
                color: {AppTheme.WHITE};
                border: none;
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                padding: 8px 16px;
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-weight: bold;
                font-family: {AppTheme.FONT_FAMILY};
                margin: 5px;
            }}
            
            QPushButton[filterButton="true"]:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #117a8b,
                    stop: 1 #0c5460
                );
            }}
            
            QPushButton[clearFilterButton="true"] {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {AppTheme.WARNING},
                    stop: 1 #e0a800
                );
                color: {AppTheme.WHITE};
                border: none;
                border-radius: {AppTheme.BORDER_RADIUS_SMALL};
                padding: 8px 16px;
                font-size: {AppTheme.FONT_SIZE_NORMAL};
                font-weight: bold;
                font-family: {AppTheme.FONT_FAMILY};
                margin: 5px;
            }}
            
            QPushButton[clearFilterButton="true"]:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #e0a800,
                    stop: 1 #b69500
                );
            }}
        """
    
    @staticmethod
    def get_complete_table_styles():
        """Retorna todos los estilos de tablas combinados"""
        return f"""
            {TableStyles.get_data_table_styles()}
            {TableStyles.get_filter_styles()}
        """
