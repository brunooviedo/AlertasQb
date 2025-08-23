"""
Gestor para integración con SQL Server
"""

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text, MetaData, Table, Column, String, DateTime, Text
from typing import Dict, Tuple, Optional
from datetime import datetime
import urllib.parse

from src.data.excel_manager import ExcelManager


class SQLManager:
    """Gestor para operaciones con SQL Server"""
    
    def __init__(self, server: str, database: str, username: Optional[str] = None, 
                 password: Optional[str] = None, table: str = "alertas_geotecnicas"):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.table = table
        self.engine = None
        self.excel_manager = ExcelManager()
        
    def _create_connection_string(self) -> str:
        """Crea la cadena de conexión"""
        if self.username and self.password:
            # Conexión con autenticación SQL
            password_encoded = urllib.parse.quote_plus(self.password)
            connection_string = (
                f"mssql+pyodbc://{self.username}:{password_encoded}@{self.server}/"
                f"{self.database}?driver=ODBC+Driver+17+for+SQL+Server"
            )
        else:
            # Conexión con autenticación Windows
            connection_string = (
                f"mssql+pyodbc://@{self.server}/{self.database}?"
                f"driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
            )
            
        return connection_string
        
    def _get_engine(self) -> sqlalchemy.Engine:
        """Obtiene el engine de SQLAlchemy"""
        if self.engine is None:
            connection_string = self._create_connection_string()
            self.engine = create_engine(connection_string, echo=False)
        return self.engine
        
    def test_connection(self) -> Tuple[bool, str]:
        """Prueba la conexión a la base de datos"""
        try:
            engine = self._get_engine()
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                return True, "Conexión exitosa"
        except Exception as e:
            return False, str(e)
            
    def _create_table_if_not_exists(self) -> bool:
        """Crea la tabla si no existe"""
        try:
            engine = self._get_engine()
            
            metadata = MetaData()
            
            # Definir la estructura de la tabla
            alerts_table = Table(
                self.table, metadata,
                Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True),
                Column('FechaHora', String(50)),
                Column('TipoAlerta', String(20)),
                Column('Condicion', String(20)),
                Column('Respaldo', Text),
                Column('Colapso', String(10)),
                Column('FechaHoraColapso', String(50)),
                Column('Evacuacion', String(10)),
                Column('CronologiaAnalisis', Text),
                Column('Observaciones', Text),
                Column('Usuario', String(100)),
                Column('FechaRegistro', String(50)),
                Column('FechaCreacionSQL', DateTime, default=datetime.now)
            )
            
            # Crear tabla si no existe
            metadata.create_all(engine, checkfirst=True)
            
            return True
            
        except Exception as e:
            print(f"Error creando tabla: {e}")
            return False
            
    def export_to_sql(self) -> Tuple[bool, str]:
        """Exporta datos de Excel a SQL Server"""
        try:
            # Cargar datos de Excel
            df = self.excel_manager.load_data()
            
            if df.empty:
                return False, "No hay datos para exportar"
                
            # Crear tabla si no existe
            if not self._create_table_if_not_exists():
                return False, "Error creando tabla en SQL Server"
                
            engine = self._get_engine()
            
            # Agregar columna de timestamp para SQL
            df['FechaCreacionSQL'] = datetime.now()
            
            # Verificar duplicados en SQL
            with engine.connect() as conn:
                # Obtener datos existentes
                try:
                    existing_df = pd.read_sql(
                        f"SELECT FechaHora, TipoAlerta, Observaciones FROM {self.table}",
                        conn
                    )
                except:
                    existing_df = pd.DataFrame()
                    
            # Filtrar registros nuevos
            if not existing_df.empty:
                # Crear hash para comparación
                df['temp_hash'] = df['FechaHora'] + df['TipoAlerta'] + df['Observaciones']
                existing_df['temp_hash'] = (
                    existing_df['FechaHora'] + 
                    existing_df['TipoAlerta'] + 
                    existing_df['Observaciones']
                )
                
                # Filtrar solo registros nuevos
                new_df = df[~df['temp_hash'].isin(existing_df['temp_hash'])]
                new_df = new_df.drop('temp_hash', axis=1)
            else:
                new_df = df
                
            if new_df.empty:
                return True, "No hay registros nuevos para exportar"
                
            # Insertar en SQL Server
            rows_inserted = new_df.to_sql(
                self.table, 
                engine, 
                if_exists='append', 
                index=False,
                method='multi'
            )
            
            return True, f"Exportados {len(new_df)} registros a SQL Server"
            
        except Exception as e:
            return False, f"Error exportando a SQL: {str(e)}"
            
    def import_from_sql(self) -> Tuple[bool, str]:
        """Importa datos de SQL Server a Excel"""
        try:
            engine = self._get_engine()
            
            # Verificar que la tabla existe
            with engine.connect() as conn:
                try:
                    # Cargar todos los datos de SQL
                    sql_df = pd.read_sql(f"SELECT * FROM {self.table}", conn)
                    
                    if sql_df.empty:
                        return False, "No hay datos en SQL Server"
                        
                    # Remover columnas específicas de SQL
                    columns_to_remove = ['id', 'FechaCreacionSQL']
                    for col in columns_to_remove:
                        if col in sql_df.columns:
                            sql_df = sql_df.drop(col, axis=1)
                            
                except Exception as e:
                    return False, f"Error leyendo tabla SQL: {str(e)}"
                    
            # Cargar datos existentes de Excel
            excel_df = self.excel_manager.load_data()
            
            # Combinar datos
            if excel_df.empty:
                combined_df = sql_df
            else:
                # Evitar duplicados
                excel_df['temp_hash'] = (
                    excel_df['FechaHora'] + 
                    excel_df['TipoAlerta'] + 
                    excel_df['Observaciones']
                )
                sql_df['temp_hash'] = (
                    sql_df['FechaHora'] + 
                    sql_df['TipoAlerta'] + 
                    sql_df['Observaciones']
                )
                
                # Filtrar registros nuevos de SQL
                new_sql_records = sql_df[~sql_df['temp_hash'].isin(excel_df['temp_hash'])]
                new_sql_records = new_sql_records.drop('temp_hash', axis=1)
                excel_df = excel_df.drop('temp_hash', axis=1)
                
                if new_sql_records.empty:
                    return True, "No hay registros nuevos en SQL Server"
                    
                combined_df = pd.concat([excel_df, new_sql_records], ignore_index=True)
                
            # Ordenar por fecha
            if 'FechaHora' in combined_df.columns:
                combined_df['FechaHora_dt'] = pd.to_datetime(
                    combined_df['FechaHora'], format='%d/%m/%Y %H:%M:%S', errors='coerce'
                )
                combined_df = combined_df.sort_values('FechaHora_dt', ascending=True)
                combined_df = combined_df.drop('FechaHora_dt', axis=1)
                
            # Guardar en Excel
            self.excel_manager._save_formatted_excel(combined_df)
            
            new_records = len(sql_df) if excel_df.empty else len(new_sql_records)
            return True, f"Importados {new_records} registros desde SQL Server"
            
        except Exception as e:
            return False, f"Error importando desde SQL: {str(e)}"
            
    def sync_bidirectional(self) -> Tuple[bool, str]:
        """Sincronización bidireccional entre Excel y SQL"""
        try:
            # Primero exportar de Excel a SQL
            export_success, export_msg = self.export_to_sql()
            
            if not export_success:
                return False, f"Error en exportación: {export_msg}"
                
            # Luego importar de SQL a Excel
            import_success, import_msg = self.import_from_sql()
            
            if not import_success:
                return False, f"Error en importación: {import_msg}"
                
            return True, f"Sincronización completada. {export_msg}. {import_msg}"
            
        except Exception as e:
            return False, f"Error en sincronización: {str(e)}"
            
    def execute_custom_query(self, query: str) -> Tuple[bool, str, pd.DataFrame]:
        """Ejecuta una consulta personalizada"""
        try:
            engine = self._get_engine()
            
            with engine.connect() as conn:
                df = pd.read_sql(query, conn)
                
            return True, "Consulta ejecutada correctamente", df
            
        except Exception as e:
            return False, f"Error ejecutando consulta: {str(e)}", pd.DataFrame()
            
    def get_sql_statistics(self) -> Dict:
        """Obtiene estadísticas de la base de datos SQL"""
        try:
            engine = self._get_engine()
            
            with engine.connect() as conn:
                # Estadísticas básicas
                stats = {}
                
                # Total de registros
                total_result = conn.execute(text(f"SELECT COUNT(*) FROM {self.table}"))
                stats['total_records'] = total_result.scalar()
                
                # Por tipo de alerta
                type_result = conn.execute(text(
                    f"SELECT TipoAlerta, COUNT(*) as count FROM {self.table} "
                    f"GROUP BY TipoAlerta"
                ))
                stats['by_type'] = {row[0]: row[1] for row in type_result}
                
                # Por usuario
                user_result = conn.execute(text(
                    f"SELECT Usuario, COUNT(*) as count FROM {self.table} "
                    f"GROUP BY Usuario ORDER BY count DESC"
                ))
                stats['by_user'] = {row[0]: row[1] for row in user_result}
                
                # Registros recientes (último mes)
                recent_result = conn.execute(text(
                    f"SELECT COUNT(*) FROM {self.table} "
                    f"WHERE FechaCreacionSQL >= DATEADD(month, -1, GETDATE())"
                ))
                stats['recent_records'] = recent_result.scalar()
                
            return stats
            
        except Exception as e:
            print(f"Error obteniendo estadísticas SQL: {e}")
            return {}
            
    def backup_to_excel(self, backup_path: str) -> Tuple[bool, str]:
        """Crea un backup de SQL a Excel"""
        try:
            engine = self._get_engine()
            
            with engine.connect() as conn:
                df = pd.read_sql(f"SELECT * FROM {self.table}", conn)
                
            if df.empty:
                return False, "No hay datos para respaldar"
                
            # Crear backup con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{backup_path}/backup_sql_{timestamp}.xlsx"
            
            # Remover columnas específicas de SQL si existen
            columns_to_remove = ['id', 'FechaCreacionSQL']
            for col in columns_to_remove:
                if col in df.columns:
                    df = df.drop(col, axis=1)
                    
            # Usar el método de formateo del ExcelManager
            self.excel_manager._save_formatted_excel_to_path(df, backup_file)
            
            return True, f"Backup creado: {backup_file}"
            
        except Exception as e:
            return False, f"Error creando backup: {str(e)}"
