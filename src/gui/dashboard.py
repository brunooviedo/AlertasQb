"""
Dashboard Widget - Mejorado para múltiples años
Proporciona una vista de dashboard con KPIs, gráficos y filtros de datos
"""

import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QFrame, QScrollArea, QGridLayout,
                               QComboBox, QGroupBox, QSizePolicy)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPalette, QPixmap
import pandas as pd
import numpy as np

# Importaciones optimizadas - las librerías pesadas ya están precargadas en main.py
MATPLOTLIB_AVAILABLE = None
matplotlib = None
plt = None
Figure = None
sns = None
FigureCanvas = None

def _load_matplotlib():
    """Carga matplotlib - optimizado para librerías precargadas"""
    global MATPLOTLIB_AVAILABLE, matplotlib, plt, Figure, sns, FigureCanvas
    
    if MATPLOTLIB_AVAILABLE is not None:
        return MATPLOTLIB_AVAILABLE
    
    try:
        # Las librerías ya están precargadas, solo necesitamos importarlas
        import matplotlib as mpl
        import matplotlib.pyplot as pyplot
        from matplotlib.figure import Figure as MatplotlibFigure
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        
        # Asignar a variables globales (configuración ya hecha en main.py)
        matplotlib = mpl
        plt = pyplot
        Figure = MatplotlibFigure
        FigureCanvas = FigureCanvasAgg
        
        # Importar seaborn opcionalmente (también precargado)
        try:
            import seaborn
            sns = seaborn
        except ImportError:
            sns = None
        
        MATPLOTLIB_AVAILABLE = True
        print("✓ matplotlib cargado desde precarga (optimizado)")
        
    except ImportError as e:
        print(f"⚠ matplotlib no disponible: {e}")
        MATPLOTLIB_AVAILABLE = False
    
    return MATPLOTLIB_AVAILABLE

# Importar módulos adicionales
import io
from datetime import datetime, timedelta
from src.data.excel_manager import ExcelManager

class KPIWidget(QFrame):
    """Widget para mostrar un KPI individual"""
    
    def __init__(self, title, value, color="#4CAF50"):
        super().__init__()
        self.setFrameStyle(QFrame.Box)
        self.setFixedHeight(120)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #ffffff, stop:1 #f5f5f5);
                border: 2px solid {color};
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        
        # Título
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 12px;")
        
        # Valor
        self.value_label = QLabel(value)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 24px;")
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        self.setLayout(layout)
        
    def update_value(self, value):
        """Actualiza el valor del KPI"""
        self.value_label.setText(str(value))

class ChartWidget(QFrame):
    """Widget para mostrar gráficos"""
    
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.setFrameStyle(QFrame.Box)
        # Container principal con altura más moderada
        self.setMinimumHeight(700)  # Reducido para mejor proporción
        self.setMinimumWidth(500)   # Mantener ancho
        self.setMaximumHeight(670)  # Aumentado también
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # Más margen
        
        # Título del gráfico
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # Inicializar canvas sin cargar matplotlib aún
        self.canvas = QLabel()
        self.canvas.setAlignment(Qt.AlignCenter)
        self.canvas.setMinimumSize(900, 600)  # Canvas menos alto pero mismo ancho
        self.canvas.setStyleSheet("border: 1px solid #ddd; background: white;")
        self.canvas.setText("Cargando gráfico...")
        layout.addWidget(self.canvas)
        
        # Figura se creará cuando se necesite
        self.figure = None
        
        self.setLayout(layout)
        
    def update_chart(self, data):
        """Actualiza el gráfico con nuevos datos"""
        if MATPLOTLIB_AVAILABLE and hasattr(self, 'figure'):
            self.figure.clear()
            # Implementación específica en subclases
            self._render_to_label()
        else:
            # No hacer nada si matplotlib no está disponible
            pass
            
    def _render_to_label(self):
        """Convierte la figura de matplotlib a imagen y la muestra en el QLabel"""
        # Cargar matplotlib dinámicamente si no está cargado
        if not _load_matplotlib() or not hasattr(self, 'canvas'):
            self.canvas.setText("📊 Gráficos no disponibles")
            return
            
        # Crear figura si no existe
        if self.figure is None:
            self.figure = Figure(figsize=(12, 8), dpi=75)
            self.figure.patch.set_facecolor('white')
            # Crear canvas de matplotlib para asegurar renderizado correcto
            self.figure.set_canvas(FigureCanvas(self.figure))
            
        try:
            # Asegurar que la figura esté completamente renderizada
            self.figure.canvas.draw()
            
            # Guardar la figura en un buffer de memoria con padding máximo para mostrar todo
            buf = io.BytesIO()
            self.figure.savefig(buf, format='png', dpi=90, bbox_inches='tight', 
                               pad_inches=0.8, facecolor='white', edgecolor='none',
                               transparent=False)  # Configuraciones específicas para ejecutables
            buf.seek(0)
            
            # Crear QPixmap desde el buffer
            pixmap = QPixmap()
            success = pixmap.loadFromData(buf.getvalue())
            
            if success and not pixmap.isNull():
                # Escalar imagen para ajustar al contenedor manteniendo proporción
                canvas_size = self.canvas.size()
                scaled_pixmap = pixmap.scaled(canvas_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.canvas.setPixmap(scaled_pixmap)
                print(f"✓ Gráfico renderizado exitosamente ({pixmap.width()}x{pixmap.height()})")
            else:
                print("✗ Error: No se pudo cargar la imagen del gráfico")
                self.canvas.setText("Error: Imagen no válida")
            
            buf.close()
        except Exception as e:
            print(f"✗ Error renderizando gráfico: {e}")
            self.canvas.setText(f"Error al renderizar: {str(e)}")

class Dashboard(QWidget):
    """
    Widget de Dashboard principal mejorado para múltiples años
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.excel_manager = ExcelManager()
        self.current_data = pd.DataFrame()
        self.data_loaded = False  # Flag para controlar carga diferida
        self.refresh_in_progress = False  # Flag para evitar refresh múltiples
        self.setup_ui()
        self.apply_styles()
        # NO cargar datos iniciales aquí - se hace cuando se muestra la pestaña
        
    def ensure_data_loaded(self):
        """Cargar datos solo cuando se necesiten (lazy loading optimizado)"""
        if not self.data_loaded:
            print("📊 Cargando datos del dashboard por primera vez...")
            self.load_initial_data()
            self.data_loaded = True
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header con filtros
        header_layout = QHBoxLayout()
        
        # Título
        title = QLabel("Dashboard de Alertas Geotécnicas")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E7D4F; margin-bottom: 20px;")
        
        # Botón de actualizar
        self.refresh_button = QPushButton("🔄 Actualizar")
        self.refresh_button.clicked.connect(self.reload_data)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_button)
        
        layout.addLayout(header_layout)
        
        # Panel de filtros
        filter_group = QGroupBox("Filtros")
        filter_layout = QHBoxLayout()
        
        # Filtro por año
        filter_layout.addWidget(QLabel("Año:"))
        self.year_combo = QComboBox()
        self.year_combo.currentTextChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.year_combo)
        
        # Filtro por mes
        filter_layout.addWidget(QLabel("Mes:"))
        self.month_combo = QComboBox()
        self.month_combo.addItems([
            "Todos", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])
        self.month_combo.currentTextChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.month_combo)
        
        # Filtro por tipo de alerta
        filter_layout.addWidget(QLabel("Tipo:"))
        self.type_combo = QComboBox()
        self.type_combo.currentTextChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.type_combo)
        
        filter_layout.addStretch()
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        # Scroll area para el contenido
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # KPIs
        self.kpi_layout = QHBoxLayout()
        self.setup_kpis()
        scroll_layout.addLayout(self.kpi_layout)
        
        # Gráficos
        self.charts_layout = QGridLayout()
        self.setup_charts()
        scroll_layout.addLayout(self.charts_layout)
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        self.setLayout(layout)
        
    def load_initial_data(self):
        """Carga los datos iniciales desde Excel"""
        self.update_data(self.excel_manager)
        
    def setup_kpis(self):
        """Configura los widgets de KPI"""
        self.total_kpi = KPIWidget("Total Alertas", "0", "#2196F3")
        self.red_kpi = KPIWidget("Alertas Rojas", "0", "#F44336")
        self.orange_kpi = KPIWidget("Alertas Naranjas", "0", "#FF9800")
        self.yellow_kpi = KPIWidget("Alertas Amarillas", "0", "#FFEB3B")
        self.active_user_kpi = KPIWidget("Usuario Más Activo", "N/A", "#9C27B0")
        self.recent_kpi = KPIWidget("Alertas Últimos 30 días", "0", "#9A0707")
        
        self.kpi_layout.addWidget(self.total_kpi)
        self.kpi_layout.addWidget(self.red_kpi)
        self.kpi_layout.addWidget(self.orange_kpi)
        self.kpi_layout.addWidget(self.yellow_kpi)
        self.kpi_layout.addWidget(self.active_user_kpi)
        self.kpi_layout.addWidget(self.recent_kpi)

        # AÑADIR ESTA LÍNEA para espaciado entre contadores:
        self.kpi_layout.setSpacing(15)  # ← NUEVO: espaciado horizontal entre KPIs
        
    def setup_charts(self):
        """Configura los widgets de gráficos"""
        self.alert_type_chart = ChartWidget("Distribución por Tipo de Alerta")
        self.condition_chart = ChartWidget("Distribución por Condición")
        self.users_chart = ChartWidget("Usuarios Más Activos")
        self.monthly_chart = ChartWidget("Alertas por Mes")
        
        self.charts_layout.addWidget(self.alert_type_chart, 0, 0)
        self.charts_layout.addWidget(self.condition_chart, 0, 1)
        self.charts_layout.addWidget(self.users_chart, 1, 0)
        self.charts_layout.addWidget(self.monthly_chart, 1, 1)
        
    def apply_styles(self):
        """Aplica estilos consistentes"""
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #c9c9c9;
                border-radius: 8px;
                margin-top: 14px;
                padding-top: 8px;
                background: #fcfcfc;
                color: #000000;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
                color: #2E7D4F;
            }
            QComboBox {
                border: 1px solid #d2d2d2;
                border-radius: 6px;
                padding: 6px 8px;
                font-size: 13px;
                background: #ffffff;
                color: #000000;
                min-width: 80px;
            }
            QComboBox:focus {
                border-color: #4CAF50;
                outline: none;
            }
            QPushButton {
                background-color: #4CAF50;
                color: #ffffff;
                border: none;
                padding: 8px 18px;
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
                min-width: 110px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QLabel {
                font-size: 13px;
                color: #000000;
            }
            QScrollArea {
                border: 1px solid #d2d2d2;
                border-radius: 6px;
                background: #ffffff;
            }
        """)
        
    def on_filter_changed(self):
        """Maneja cambios en los filtros"""
        self.refresh_charts()
        
    def reload_data(self):
        """Recarga los datos desde Excel"""
        self.update_data(self.excel_manager)
        
    def get_filtered_data(self):
        """Obtiene datos filtrados según los controles con validación mejorada"""
        if self.current_data.empty:
            return pd.DataFrame()
        
        filtered_data = self.current_data.copy()
        original_count = len(filtered_data)
        
        # Filtro por año
        year_filter = self.year_combo.currentText().strip()
        if year_filter and year_filter != "Todos los años":
            try:
                year = int(year_filter)
                filtered_data = filtered_data[filtered_data['Año'] == year]
                print(f"Filtro año {year}: {len(filtered_data)} alertas")
            except (ValueError, TypeError):
                print(f"⚠️ Error al filtrar año: '{year_filter}' no es válido")
        
        # Filtro por mes
        month_filter = self.month_combo.currentText().strip()
        if month_filter and month_filter != "Todos":
            month_num = self.month_combo.currentIndex()  # 0=Todos, 1=Enero, etc.
            if month_num > 0:  # No filtrar si es "Todos"
                # Primero verificar si hay datos para este mes en el año seleccionado
                before_month_filter = len(filtered_data)
                filtered_data = filtered_data[filtered_data['Mes'] == month_num]
                after_month_filter = len(filtered_data)
                
                print(f"Filtro mes {month_filter} ({month_num}): {after_month_filter} alertas")
                
                # Si no hay datos para el mes seleccionado, mostrar mensaje
                if before_month_filter > 0 and after_month_filter == 0:
                    year_text = f"del año {year_filter}" if year_filter and year_filter != "Todos los años" else ""
                    print(f"⚠️ No se encontraron alertas para {month_filter} {year_text}")
        
        # Filtro por tipo
        type_filter = self.type_combo.currentText().strip()
        if type_filter and type_filter != "Todos":
            before_type_filter = len(filtered_data)
            filtered_data = filtered_data[filtered_data['TipoAlerta'] == type_filter]
            after_type_filter = len(filtered_data)
            
            print(f"Filtro tipo {type_filter}: {after_type_filter} alertas")
            
            # Si no hay datos para el tipo seleccionado, mostrar mensaje
            if before_type_filter > 0 and after_type_filter == 0:
                filters_text = []
                if year_filter and year_filter != "Todos los años":
                    filters_text.append(f"año {year_filter}")
                if month_filter and month_filter != "Todos":
                    filters_text.append(f"mes {month_filter}")
                
                context = " para " + " y ".join(filters_text) if filters_text else ""
                print(f"⚠️ No se encontraron alertas {type_filter.lower()}s{context}")
        
        # Resumen final del filtrado
        if len(filtered_data) == 0 and original_count > 0:
            print(f"🔍 Filtros aplicados no encontraron resultados. Total disponible: {original_count} alertas")
        elif len(filtered_data) < original_count:
            print(f"📊 Mostrando {len(filtered_data)} de {original_count} alertas totales")
        
        return filtered_data
        
    def update_data(self, excel_manager):
        """Actualiza los datos del dashboard"""
        try:
            # Cargar datos del Excel
            data = excel_manager.load_data()
            print(f"Dashboard: Datos cargados desde Excel: {len(data)} filas")
            
            if data.empty:
                self.current_data = pd.DataFrame()
                self.update_filters(refresh_charts=False)
                self.refresh_charts()  # Un solo refresh
                return
            
            # Los datos ya vienen procesados del ExcelManager con Año y Mes
            data_processed = data.copy()
            
            # Verificar que las columnas necesarias están presentes
            required_columns = ['FechaHora', 'TipoAlerta', 'Año', 'Mes', 'Usuario']
            missing_columns = [col for col in required_columns if col not in data_processed.columns]
            
            if missing_columns:
                print(f"⚠️ Columnas faltantes: {missing_columns}")
                # Si faltan Año o Mes, el ExcelManager no las creó correctamente
                print(f"📋 Columnas disponibles: {list(data_processed.columns)}")
            
            # Solo procesar FechaHoraColapso si existe
            if 'FechaHoraColapso' in data_processed.columns:
                data_processed['FechaHoraColapso'] = pd.to_datetime(
                    data_processed['FechaHoraColapso'], errors='coerce'
                )
                
            # Mostrar estadísticas de procesamiento
            print(f"Dashboard: Datos procesados:")
            print(f"  - Total filas: {len(data_processed)}")
            if 'Año' in data_processed.columns:
                years = sorted([int(year) for year in data_processed['Año'].dropna().unique()])
                print(f"  - Años disponibles: {years}")
            if 'TipoAlerta' in data_processed.columns:
                tipos = data_processed['TipoAlerta'].value_counts().head(10).to_dict()
                print(f"  - Tipos de alerta: {tipos}")
            if 'Condicion' in data_processed.columns:
                condiciones = data_processed['Condicion'].value_counts().head(10).to_dict()
                print(f"  - Condiciones: {condiciones}")
                
            self.current_data = data_processed
            print("🔄 Actualizando filtros y gráficos...")
            self.update_filters(refresh_charts=False)  # No refresh automático
            self.refresh_charts()  # Un solo refresh al final
            
        except Exception as e:
            print(f"Error actualizando dashboard: {e}")
            import traceback
            traceback.print_exc()
            self.current_data = pd.DataFrame()
            
    def update_filters(self, refresh_charts=True):
        """Actualiza las opciones de los filtros"""
        try:
            # Desconectar signals temporalmente para evitar refresh múltiples
            self.year_combo.currentTextChanged.disconnect()
            self.month_combo.currentTextChanged.disconnect()
            self.type_combo.currentTextChanged.disconnect()
            
            # Actualizar filtro de años
            self.year_combo.clear()
            self.year_combo.addItem("Todos los años")
            
            if not self.current_data.empty and 'Año' in self.current_data.columns:
                years = sorted([int(year) for year in self.current_data['Año'].dropna().unique()])
                for year in years:
                    self.year_combo.addItem(str(year))
                print(f"✅ Años cargados en filtro: {years}")
            
            # Actualizar filtro de tipos
            self.type_combo.clear()
            self.type_combo.addItem("Todos")
            
            if not self.current_data.empty and 'TipoAlerta' in self.current_data.columns:
                types = sorted(self.current_data['TipoAlerta'].dropna().unique())
                for alert_type in types:
                    self.type_combo.addItem(str(alert_type))
                print(f"✅ Tipos cargados en filtro: {types}")
                
            # Reconectar signals
            self.year_combo.currentTextChanged.connect(self.on_filter_changed)
            self.month_combo.currentTextChanged.connect(self.on_filter_changed)
            self.type_combo.currentTextChanged.connect(self.on_filter_changed)
                
            print(f"✅ Filtros actualizados correctamente")
            
            # Solo hacer refresh si se solicita (evitar spam de renders)
            if refresh_charts:
                print("🔄 Auto-refresh después de actualizar filtros")
                self.refresh_charts()
            
        except Exception as e:
            print(f"❌ Error actualizando filtros: {e}")
            import traceback
            traceback.print_exc()
            types = sorted(self.current_data['TipoAlerta'].dropna().unique())
            for alert_type in types:
                self.type_combo.addItem(str(alert_type))
                
    def refresh_charts(self):
        """Actualiza todos los gráficos y KPIs con protección anti-spam"""
        if self.refresh_in_progress:
            print("🚫 Refresh ya en progreso, evitando render duplicado")
            return
            
        self.refresh_in_progress = True
        try:
            print("🎨 Iniciando refresh de gráficos...")
            filtered_data = self.get_filtered_data()
            self.update_kpis(filtered_data)
            self.update_charts(filtered_data)
            print("✅ Refresh de gráficos completado")
        finally:
            self.refresh_in_progress = False
        
    def update_kpis(self, data):
        """Actualiza los valores de los KPIs"""
        if data.empty:
            self.total_kpi.update_value("0")
            self.red_kpi.update_value("0")
            self.orange_kpi.update_value("0")
            self.yellow_kpi.update_value("0")
            self.active_user_kpi.update_value("N/A")
            self.recent_kpi.update_value("0")
            return
        
        # Total de alertas
        total = len(data)
        self.total_kpi.update_value(str(total))
        
        # Alertas por tipo
        if 'TipoAlerta' in data.columns:
            red_count = len(data[data['TipoAlerta'] == 'Roja'])
            orange_count = len(data[data['TipoAlerta'] == 'Naranja'])
            yellow_count = len(data[data['TipoAlerta'] == 'Amarilla'])
            
            self.red_kpi.update_value(str(red_count))
            self.orange_kpi.update_value(str(orange_count))
            self.yellow_kpi.update_value(str(yellow_count))
        
        # Usuario más activo
        if 'Usuario' in data.columns:
            user_counts = data['Usuario'].value_counts()
            if len(user_counts) > 0:
                most_active = user_counts.index[0]
                count = user_counts.iloc[0]
                self.active_user_kpi.update_value(f"{most_active} ({count})")
            else:
                self.active_user_kpi.update_value("N/A")
        
        # Alertas recientes (últimos 30 días)
        if 'FechaHora' in data.columns and not data.empty:
            try:
                # Convertir FechaHora a datetime si no lo está
                today = datetime.now().date()  # Solo la fecha, sin hora
                # Usar 31 días para incluir alertas del día 30 completo
                thirty_days_ago_date = today - timedelta(days=31)  # Cambiar a 31 para incluir más días
                
                # Convertir la columna a datetime temporalmente para la comparación
                if data['FechaHora'].dtype == 'object':
                    fecha_dt = pd.to_datetime(data['FechaHora'], errors='coerce')
                    # Comparar solo las fechas (sin hora) para incluir todo el día
                    fecha_dates = fecha_dt.dt.date
                    recent_data = data[fecha_dates >= thirty_days_ago_date]
                else:
                    fecha_dates = data['FechaHora'].dt.date
                    recent_data = data[fecha_dates >= thirty_days_ago_date]
                
                self.recent_kpi.update_value(str(len(recent_data)))
                print(f"📊 KPI Últimos 30 días: {len(recent_data)} alertas (desde {thirty_days_ago_date})")
            except Exception as e:
                print(f"Error calculando alertas recientes: {e}")
                self.recent_kpi.update_value("0")
            
    def update_charts(self, data):
        """Actualiza los gráficos con los datos filtrados"""
        # Cargar matplotlib dinámicamente cuando se necesite
        if not _load_matplotlib():
            # Si matplotlib no está disponible, mostrar mensaje en todos los gráficos
            for chart in [self.alert_type_chart, self.condition_chart, 
                         self.users_chart, self.monthly_chart]:
                chart.canvas.setText("📊 Gráficos no disponibles\n\nInstalando matplotlib...")
            return
            
        if data.empty:
            # Limpiar gráficos si no hay datos
            for chart in [self.alert_type_chart, self.condition_chart, 
                         self.users_chart, self.monthly_chart]:
                if chart.figure is None:
                    chart.figure = Figure(figsize=(12, 8), dpi=75)
                    chart.figure.patch.set_facecolor('white')
                    chart.figure.set_canvas(FigureCanvas(chart.figure))
                    
                chart.figure.clear()
                ax = chart.figure.add_subplot(111)
                ax.text(0.5, 0.5, 'Sin datos para mostrar', 
                       horizontalalignment='center', verticalalignment='center',
                       transform=ax.transAxes, fontsize=14, color='gray')
                ax.set_xticks([])
                ax.set_yticks([])
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
                ax.spines['left'].set_visible(False)
                chart.figure.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.3)  # Márgenes extremos
                chart.figure.tight_layout(pad=6.0)  # Padding extremo para etiquetas
                chart._render_to_label()
            return
        
        # Gráfico de distribución por tipo
        self.update_type_chart(data)
        
        # Gráfico de distribución por condición
        self.update_condition_chart(data)
        
        # Gráfico de usuarios más activos
        self.update_users_chart(data)
        
        # Gráfico de alertas por mes
        self.update_monthly_chart(data)
        
    def update_type_chart(self, data):
        """Actualiza gráfico de tipos de alerta"""
        # Crear figura si no existe
        if self.alert_type_chart.figure is None:
            self.alert_type_chart.figure = Figure(figsize=(12, 8), dpi=75)
            self.alert_type_chart.figure.patch.set_facecolor('white')
            self.alert_type_chart.figure.set_canvas(FigureCanvas(self.alert_type_chart.figure))
            
        self.alert_type_chart.figure.clear()
        
        if 'TipoAlerta' in data.columns:
            type_counts = data['TipoAlerta'].value_counts()
            print(f"DEBUG - Tipos de alerta encontrados: {type_counts}")  # Debug
            
            if len(type_counts) > 0:
                ax = self.alert_type_chart.figure.add_subplot(111)
                
                # Definir colores para cada tipo de alerta (más opciones)
                alerta_colores = {
                    'Amarilla': '#FFD600',      # Amarillo brillante
                    'Amarillo': '#FFD600',      # Por si viene como "Amarillo"
                    'Naranja': '#FF9040',       # Naranja corporativo Teck
                    'Roja': '#FF4040',          # Rojo vibrante
                    'Rojo': '#FF4040',          # Por si viene como "Rojo"
                    'Verde': '#00A26A',         # Verde corporativo Teck
                    'Azul': '#3153E4',          # Azul corporativo Teck
                    'Alta': '#FF4040',          # Roja para "Alta"
                    'Media': '#FF9040',         # Naranja para "Media"
                    'Baja': '#FFD600',          # Amarillo para "Baja"
                    'Crítica': '#8B0000',       # Rojo oscuro para "Crítica"
                }
                
                # Definir colores de fondo suaves para cada alerta
                fondo_colores = {
                    'Amarilla': '#FFFDE7',     'Amarillo': '#FFFDE7',
                    'Naranja': '#FFF3E0',      
                    'Roja': '#FFEBEE',         'Rojo': '#FFEBEE',
                    'Verde': '#E8F5E8',        
                    'Azul': '#E3F2FD',
                    'Alta': '#FFEBEE',
                    'Media': '#FFF3E0',
                    'Baja': '#FFFDE7',
                    'Crítica': '#FFCDD2'
                }
                
                # Función para determinar color de texto con contraste
                def get_text_color(tipo_alerta):
                    # Negro para colores claros
                    colores_claros = ['Amarilla', 'Amarillo', 'Verde', 'Baja']
                    if tipo_alerta in colores_claros:
                        return 'black'
                    return 'white'
                
                # Obtener colores para las porciones del pie
                colors_list = []
                text_colors = []
                labels_list = []
                values_list = []
                
                for tipo in type_counts.index:
                    if type_counts[tipo] > 0:  # Solo incluir tipos con datos
                        colors_list.append(alerta_colores.get(tipo, '#CCCCCC'))
                        text_colors.append(get_text_color(tipo))
                        labels_list.append(tipo)
                        values_list.append(type_counts[tipo])
                
                print(f"DEBUG - Labels: {labels_list}, Values: {values_list}")  # Debug
                
                # Solo proceder si hay datos para mostrar
                if len(labels_list) > 0:
                    # Determinar color de fondo (usar el tipo más común)
                    tipo_principal = labels_list[0]  # El más frecuente
                    fondo_color = fondo_colores.get(tipo_principal, '#F5F5F5')
                    ax.set_facecolor(fondo_color)
                    
                    # Crear gráfico de pie con colores personalizados
                    wedges, texts, autotexts = ax.pie(
                        values_list,
                        labels=labels_list,
                        autopct='%1.1f%%',
                        startangle=90,
                        colors=colors_list,
                        textprops={'fontsize': 9}
                    )
                    
                    # Aplicar colores de texto con contraste para cada porción
                    for i, (autotext, text) in enumerate(zip(autotexts, texts)):
                        if i < len(text_colors):
                            color = text_colors[i]
                            autotext.set_color(color)
                            autotext.set_weight('bold')
                            autotext.set_fontsize(10)
                            # Las etiquetas de la leyenda siempre en negro para visibilidad
                            text.set_color('black')
                            text.set_fontsize(9)
                            text.set_weight('bold')
                
                    ax.set_title('Distribución por Tipo de Alerta', fontsize=12, fontweight='bold', pad=20)
                else:
                    # Si no hay datos, mostrar mensaje
                    ax.text(0.5, 0.5, 'Sin datos para mostrar', 
                           horizontalalignment='center', verticalalignment='center',
                           transform=ax.transAxes, fontsize=12)
                    ax.set_title('Distribución por Tipo de Alerta', fontsize=12, fontweight='bold', pad=20)
                
        self.alert_type_chart.figure.subplots_adjust(left=0.15, right=0.85, top=0.85, bottom=0.25)  # Márgenes generosos
        self.alert_type_chart.figure.tight_layout(pad=6.0)  # Padding extremo para etiquetas
        self.alert_type_chart._render_to_label()
            
    def update_condition_chart(self, data):
        """Actualiza gráfico de condiciones de alerta"""
        # Crear figura si no existe
        if self.condition_chart.figure is None:
            self.condition_chart.figure = Figure(figsize=(12, 8), dpi=75)
            self.condition_chart.figure.patch.set_facecolor('white')
            self.condition_chart.figure.set_canvas(FigureCanvas(self.condition_chart.figure))
            
        self.condition_chart.figure.clear()
        
        if 'Condicion' in data.columns:
            condition_counts = data['Condicion'].value_counts()
            if len(condition_counts) > 0:
                ax = self.condition_chart.figure.add_subplot(111)
                
                # Colores para las diferentes condiciones
                colors = {
                    'Crítica': '#F44336', 
                    'Progresiva': '#FF9800', 
                    'Transgresiva': '#FFEB3B', 
                    'Progresiva-Crítica': '#E91E63', 
                    'Transgresiva-Progresiva': '#FF5722', 
                    'Regresiva': '#4CAF50'
                }
                
                # Crear barras con colores
                bar_colors = [colors.get(condition, '#9E9E9E') for condition in condition_counts.index]
                bars = ax.bar(range(len(condition_counts)), condition_counts.values, color=bar_colors)
                
                # Configurar ejes y etiquetas
                ax.set_xticks(range(len(condition_counts)))
                ax.set_xticklabels(condition_counts.index, rotation=45, ha='right', fontsize=9)
                ax.set_ylabel('Cantidad', fontsize=10)
                ax.set_title('Distribución por Condición', fontsize=12, fontweight='bold', pad=20)
                
                # Agregar valores en las barras
                for bar, value in zip(bars, condition_counts.values):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + max(condition_counts.values) * 0.01,
                           f'{int(value)}', ha='center', va='bottom', fontsize=8)
                
                # Ajustar diseño
                ax.grid(True, alpha=0.3, axis='y')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                
        self.condition_chart.figure.subplots_adjust(left=0.15, right=0.85, top=0.85, bottom=0.25)  # Márgenes generosos
        self.condition_chart.figure.tight_layout(pad=6.0)  # Padding extremo para etiquetas
        self.condition_chart._render_to_label()
            
    def update_users_chart(self, data):
        """Actualiza gráfico de usuarios más activos"""
        # Crear figura si no existe
        if self.users_chart.figure is None:
            self.users_chart.figure = Figure(figsize=(12, 8), dpi=75)
            self.users_chart.figure.patch.set_facecolor('white')
            self.users_chart.figure.set_canvas(FigureCanvas(self.users_chart.figure))
            
        self.users_chart.figure.clear()
        
        if 'Usuario' in data.columns:
            user_counts = data['Usuario'].value_counts().head(10)  # Top 10 usuarios
            if len(user_counts) > 0:
                ax = self.users_chart.figure.add_subplot(111)
                
                # Crear gráfico de barras horizontal para mejor legibilidad
                colors = plt.cm.viridis(np.linspace(0, 1, len(user_counts)))
                bars = ax.barh(range(len(user_counts)), user_counts.values, color=colors)
                
                # Configurar ejes
                ax.set_yticks(range(len(user_counts)))
                ax.set_yticklabels(user_counts.index, fontsize=9)
                ax.set_xlabel('Número de Alertas', fontsize=10)
                ax.set_title('Usuarios Más Activos', fontsize=12, fontweight='bold', pad=20)
                
                # Agregar valores en las barras
                for i, (bar, value) in enumerate(zip(bars, user_counts.values)):
                    width = bar.get_width()
                    ax.text(width + max(user_counts.values) * 0.01, bar.get_y() + bar.get_height()/2,
                           f'{int(value)}', ha='left', va='center', fontsize=9, fontweight='bold')
                
                # Mejorar apariencia
                ax.grid(True, alpha=0.3, axis='x')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.invert_yaxis()  # Mostrar el usuario con más alertas arriba
                
        self.users_chart.figure.subplots_adjust(left=0.25, right=0.85, top=0.85, bottom=0.25)  # Más espacio izquierdo para nombres
        self.users_chart.figure.tight_layout(pad=6.0)  # Padding extremo para etiquetas
        self.users_chart._render_to_label()
            
    def update_monthly_chart(self, data):
        """Actualiza gráfico de alertas por mes"""
        # Crear figura si no existe
        if self.monthly_chart.figure is None:
            self.monthly_chart.figure = Figure(figsize=(12, 8), dpi=75)
            self.monthly_chart.figure.patch.set_facecolor('white')
            self.monthly_chart.figure.set_canvas(FigureCanvas(self.monthly_chart.figure))
            
        self.monthly_chart.figure.clear()
        
        if 'Mes' in data.columns:
            # Usar la columna Mes que ya viene creada del ExcelManager
            data_with_month = data.dropna(subset=['Mes'])
            if not data_with_month.empty:
                ax = self.monthly_chart.figure.add_subplot(111)
                
                # Contar alertas por mes
                monthly_counts = data_with_month['Mes'].value_counts().sort_index()
                
                if len(monthly_counts) > 0:
                    # Nombres de los meses
                    month_names = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                                  'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
                    
                    # Asegurar que tenemos datos para todos los meses (1-12)
                    all_months = pd.Series(0, index=range(1, 13))
                    all_months.update(monthly_counts)
                    
                    # Crear gráfico de línea con área
                    months = list(range(1, 13))
                    ax.plot(months, all_months.values, marker='o', linewidth=3, 
                           markersize=8, color='#FF6B35', markerfacecolor='#FF6B35')
                    ax.fill_between(months, all_months.values, alpha=0.3, color='#FF6B35')
                    
                    # Configurar ejes
                    ax.set_xticks(months)
                    ax.set_xticklabels(month_names, fontsize=9)
                    ax.set_ylabel('Número de Alertas', fontsize=10)
                    ax.set_title('Distribución de Alertas por Mes', fontsize=12, fontweight='bold', pad=20)
                    
                    # Agregar valores en los puntos donde hay datos
                    for month, value in monthly_counts.items():
                        if value > 0:
                            ax.annotate(f'{int(value)}', 
                                       (month, value), 
                                       textcoords="offset points", 
                                       xytext=(0,10), 
                                       ha='center', 
                                       fontsize=8,
                                       fontweight='bold')
                    
                    # Mejorar apariencia
                    ax.grid(True, alpha=0.3, axis='y')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.set_xlim(0.5, 12.5)
                
        self.monthly_chart.figure.subplots_adjust(left=0.15, right=0.85, top=0.85, bottom=0.3)  # Espacio extra abajo para etiquetas de meses
        self.monthly_chart.figure.tight_layout(pad=6.0)  # Padding extremo para etiquetas
        self.monthly_chart._render_to_label()
