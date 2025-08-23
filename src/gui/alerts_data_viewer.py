"""
Visor de datos de alertas geotécnicas con estilo similar a AlertForm
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QTextEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QLabel,
    QFrame, QGroupBox, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
import pandas as pd

from src.data.excel_manager import ExcelManager


class AlertsDataViewer(QWidget):
    """Visor de datos de alertas geotécnicas"""

    def __init__(self):
        super().__init__()
        self.excel_manager = ExcelManager()
        self.setup_ui()
        self.apply_styles()
        self.load_data()

    # ---------------------------- UI SETUP ---------------------------- #
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Título
        title = QLabel("Datos de Alertas Geotécnicas")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(title)

        # Contenedor principal
        main_frame = QFrame()
        main_frame.setFrameStyle(QFrame.StyledPanel)
        main_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout = QVBoxLayout(main_frame)
        main_layout.setContentsMargins(24, 18, 24, 20)
        main_layout.setSpacing(18)

        # Grupo de controles
        controls_group = QGroupBox("Controles")
        controls_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        controls_layout = QHBoxLayout(controls_group)
        controls_layout.setContentsMargins(12, 10, 12, 12)
        controls_layout.setSpacing(12)

        # Filtros
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(12)

        # Filtro por tipo de alerta
        filter_layout.addWidget(QLabel("Filtro por tipo:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Todas", "Roja", "Naranja", "Amarilla"])
        self.filter_combo.currentTextChanged.connect(self.filter_data)
        self.filter_combo.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        filter_layout.addWidget(self.filter_combo)

        # Búsqueda
        filter_layout.addWidget(QLabel("Buscar:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar en observaciones...")
        self.search_input.textChanged.connect(self.search_data)
        self.search_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        filter_layout.addWidget(self.search_input)

        controls_layout.addLayout(filter_layout)
        controls_layout.addStretch()

        # Botón actualizar
        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.clicked.connect(self.load_data)
        controls_layout.addWidget(self.refresh_button)

        main_layout.addWidget(controls_group)

        # Grupo de datos
        data_group = QGroupBox("Alertas Registradas")
        data_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        data_layout = QVBoxLayout(data_group)
        data_layout.setContentsMargins(12, 10, 12, 12)
        data_layout.setSpacing(12)

        # Tabla
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        data_layout.addWidget(self.table)

        # Información estadística
        self.stats_label = QLabel("Cargando datos...")
        self.stats_label.setAlignment(Qt.AlignCenter)
        data_layout.addWidget(self.stats_label)

        main_layout.addWidget(data_group)

        layout.addWidget(main_frame)

        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 12, 0, 0)
        buttons_layout.setSpacing(12)
        buttons_layout.addStretch()

        self.export_button = QPushButton("Exportar Selección")
        self.export_button.clicked.connect(self.export_selected)
        self.export_button.setEnabled(False)

        self.delete_button = QPushButton("Eliminar Selección")
        self.delete_button.clicked.connect(self.delete_selected)
        self.delete_button.setEnabled(False)

        buttons_layout.addWidget(self.export_button)
        buttons_layout.addWidget(self.delete_button)
        layout.addLayout(buttons_layout)

        # Conectar señales de selección
        self.table.itemSelectionChanged.connect(self.on_selection_changed)

    # ---------------------------- STYLES ---------------------------- #
    def apply_styles(self):
        self.setStyleSheet(
            """
            QGroupBox { font-weight: bold; border: 1px solid #c9c9c9; border-radius: 8px; margin-top: 14px; padding-top: 8px; background: #fcfcfc; color: #000000; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; color: #2E7D4F; }
            QLineEdit, QComboBox { border: 1px solid #d2d2d2; border-radius: 6px; padding: 6px 8px; font-size: 13px; background: #ffffff; color: #000000; }
            QLineEdit:focus, QComboBox:focus { border-color: #4CAF50; outline: none; }
            QPushButton { background-color: #4CAF50; color: #ffffff; border: none; padding: 8px 18px; border-radius: 5px; font-size: 13px; font-weight: bold; min-width: 110px; }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:pressed { background-color: #3d8b40; }
            QPushButton:disabled { background-color: #cccccc; color: #666666; }
            QPushButton#delete_button { background-color: #f44336; }
            QPushButton#delete_button:hover { background-color: #da190b; }
            QLabel { font-size: 13px; color: #000000; }
            QTableWidget { 
                border: 1px solid #d2d2d2; 
                border-radius: 6px; 
                background: #ffffff; 
                color: #000000; 
                gridline-color: #dee2e6;
                alternate-background-color: #f8f9fa;
            }
            QTableWidget::item { 
                padding: 8px; 
                border-bottom: 1px solid #dee2e6;
                color: #212529;
            }
            QTableWidget::item:selected { 
                background-color: #4CAF50; 
                color: #ffffff; 
            }
            QHeaderView::section { 
                background-color: #e9ecef; 
                color: #495057; 
                padding: 10px; 
                border: 1px solid #dee2e6; 
                font-weight: bold; 
                font-size: 13px;
            }
            """
        )

        # Configurar ID para botón eliminar
        self.delete_button.setObjectName("delete_button")

    # ---------------------------- DATA OPERATIONS ---------------------------- #
    def load_data(self):
        """Carga los datos en la tabla"""
        try:
            self.df = self.excel_manager.load_data()
            self.original_df = self.df.copy()  # Mantener copia original para filtros
            
            if self.df.empty:
                self.table.setRowCount(0)
                self.table.setColumnCount(0)
                self.stats_label.setText("No hay datos disponibles")
                return
                
            self.populate_table(self.df)
            self.update_statistics()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error cargando datos: {e}")

    def populate_table(self, df):
        """Llena la tabla con los datos del DataFrame"""
        # Configurar tabla
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns.tolist())
        
        # Llenar datos
        for row in range(len(df)):
            for col in range(len(df.columns)):
                value = df.iloc[row, col]
                
                # Manejar valores especiales
                if pd.isna(value) or (isinstance(value, str) and value.lower() in ['nat', 'nan']):
                    display_value = ""
                else:
                    display_value = str(value)
                
                item = QTableWidgetItem(display_value)
                
                # Colorear filas según tipo de alerta
                if df.columns[col] == 'TipoAlerta':
                    if value == 'Roja':
                        item.setBackground(QColor(220, 53, 69))  # Bootstrap danger
                        item.setForeground(QColor(255, 255, 255))
                    elif value == 'Naranja':
                        item.setBackground(QColor(255, 140, 0))  # Naranja
                        item.setForeground(QColor(255, 255, 255))
                    elif value == 'Amarilla':
                        item.setBackground(QColor(255, 193, 7))  # Bootstrap warning
                        item.setForeground(QColor(33, 37, 41))
                else:
                    # Aplicar colores alternados para mejor contraste
                    if row % 2 == 0:
                        item.setBackground(QColor(248, 249, 250))  # Gris muy claro
                    else:
                        item.setBackground(QColor(255, 255, 255))  # Blanco
                    item.setForeground(QColor(33, 37, 41))  # Texto oscuro
                        
                self.table.setItem(row, col, item)
                
        # Ajustar columnas
        self.table.resizeColumnsToContents()

    def update_statistics(self):
        """Actualiza las estadísticas mostradas"""
        try:
            stats = self.excel_manager.get_statistics()
            current_total = len(self.df)
            
            self.stats_label.setText(
                f"Mostrando: {current_total} alertas | "
                f"Total en BD: {stats['total_alerts']} | "
                f"Rojas: {stats['alert_by_type'].get('Roja', 0)} | "
                f"Naranjas: {stats['alert_by_type'].get('Naranja', 0)} | "
                f"Amarillas: {stats['alert_by_type'].get('Amarilla', 0)}"
            )
        except Exception:
            self.stats_label.setText(f"Mostrando: {len(self.df)} alertas")

    # ---------------------------- FILTERS AND SEARCH ---------------------------- #
    def filter_data(self, filter_type):
        """Aplica filtro por tipo de alerta"""
        if filter_type == "Todas":
            filtered_df = self.original_df.copy()
        else:
            filtered_df = self.original_df[self.original_df['TipoAlerta'] == filter_type].copy()
        
        # Aplicar búsqueda si hay texto
        search_text = self.search_input.text().strip()
        if search_text:
            mask = filtered_df['Observaciones'].str.contains(search_text, case=False, na=False)
            filtered_df = filtered_df[mask]
        
        self.df = filtered_df
        self.populate_table(self.df)
        self.update_statistics()

    def search_data(self, search_text):
        """Aplica búsqueda en observaciones"""
        # Comenzar con filtro actual
        filter_type = self.filter_combo.currentText()
        if filter_type == "Todas":
            filtered_df = self.original_df.copy()
        else:
            filtered_df = self.original_df[self.original_df['TipoAlerta'] == filter_type].copy()
        
        # Aplicar búsqueda
        if search_text.strip():
            mask = filtered_df['Observaciones'].str.contains(search_text, case=False, na=False)
            filtered_df = filtered_df[mask]
        
        self.df = filtered_df
        self.populate_table(self.df)
        self.update_statistics()

    # ---------------------------- ACTIONS ---------------------------- #
    def on_selection_changed(self):
        """Maneja cambios en la selección de la tabla"""
        selected_rows = len(self.table.selectionModel().selectedRows())
        self.export_button.setEnabled(selected_rows > 0)
        self.delete_button.setEnabled(selected_rows > 0)

    def export_selected(self):
        """Exporta las filas seleccionadas"""
        selected_rows = [item.row() for item in self.table.selectionModel().selectedRows()]
        
        if not selected_rows:
            QMessageBox.warning(self, "Advertencia", "Seleccione al menos una fila para exportar")
            return
        
        try:
            # Crear DataFrame con filas seleccionadas
            selected_data = self.df.iloc[selected_rows]
            
            # Preguntar ubicación del archivo
            from PySide6.QtWidgets import QFileDialog
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar alertas seleccionadas",
                f"alertas_seleccionadas_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                "Excel Files (*.xlsx);;All Files (*)"
            )
            
            if file_path:
                selected_data.to_excel(file_path, index=False)
                QMessageBox.information(self, "Éxito", f"Se exportaron {len(selected_rows)} alertas correctamente")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar: {e}")

    def delete_selected(self):
        """Elimina las filas seleccionadas"""
        selected_rows = [item.row() for item in self.table.selectionModel().selectedRows()]
        
        if not selected_rows:
            QMessageBox.warning(self, "Advertencia", "Seleccione al menos una fila para eliminar")
            return
        
        reply = QMessageBox.question(
            self, 
            "Confirmar eliminación", 
            f"¿Está seguro de eliminar {len(selected_rows)} alerta(s)?\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Obtener índices originales para eliminar del Excel
                original_indices = self.df.iloc[selected_rows].index.tolist()
                
                # Eliminar del Excel (esto requiere implementar método en ExcelManager)
                success = self.excel_manager.delete_alerts_by_index(original_indices)
                
                if success:
                    QMessageBox.information(self, "Éxito", f"Se eliminaron {len(selected_rows)} alertas correctamente")
                    self.load_data()  # Recargar datos
                else:
                    QMessageBox.critical(self, "Error", "No se pudieron eliminar las alertas")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar: {e}")

    def set_read_only(self, read_only=True):
        """Configura la vista de datos en modo solo lectura"""
        # Deshabilitar botón de eliminar
        self.delete_button.setEnabled(not read_only)
        
        # Los botones de exportar y actualizar siempre deben estar habilitados
        self.export_button.setEnabled(True)
        self.refresh_button.setEnabled(True)
        
        if read_only:
            # Cambiar texto del botón de eliminar para indicar restricción
            self.delete_button.setText("🔒 Eliminar (Solo lectura)")
            
            # Agregar mensaje informativo si no existe
            if not hasattr(self, 'readonly_label'):
                from PySide6.QtWidgets import QLabel
                from PySide6.QtCore import Qt
                readonly_label = QLabel("⚠️ Usuario en modo solo lectura - Solo puede consultar y exportar datos")
                readonly_label.setAlignment(Qt.AlignCenter)
                readonly_label.setStyleSheet("""
                    QLabel {
                        background-color: #ffc107;
                        color: #856404;
                        padding: 8px;
                        border-radius: 5px;
                        font-weight: bold;
                        margin: 5px 0;
                    }
                """)
                # Insertar al inicio del layout
                layout = self.layout()
                layout.insertWidget(0, readonly_label)
                self.readonly_label = readonly_label
        else:
            self.delete_button.setText("Eliminar Selección")
            # Remover mensaje informativo si existe
            if hasattr(self, 'readonly_label'):
                self.readonly_label.setParent(None)
                delattr(self, 'readonly_label')
