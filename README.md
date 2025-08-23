# Sistema de Alertas Geotécnicas

## Descripción

Aplicación GUI de escritorio desarrollada en Python para el registro, seguimiento y análisis de alertas geotécnicas. Incluye sistema de autenticación local, almacenamiento en Excel con formato automático, dashboard interactivo con gráficos, gestión de usuarios y integración opcional con SQL Server.

## Características Principales

### 🔐 Sistema de Autenticación
- **Login seguro** con autenticación local (JSON + bcrypt)
- **Gestión de usuarios** con roles (admin/usuario)
- **Crear nuevas cuentas** con validación de datos
- **Cambio de contraseñas** con confirmación
- **Usuario por defecto**: admin / admin123
- **Formulario de Alertas Completo**:
  - Fecha y hora automática (editable)
  - Tipos de alerta: Amarilla, Naranja, Roja (con colores automáticos en Excel)
  - Condiciones: transgresiva, progresiva, crítica
  - Respaldo de archivos PowerPoint
  - Registro de colapsos y evacuaciones
  - Análisis cronológico y observaciones
- **Almacenamiento Excel Avanzado**:
  - Formato automático con colores por tipo de alerta
  - Detección de duplicados configurable
  - Orden cronológico automático
  - Importación/exportación con validación
- **Dashboard Interactivo**:
  - Gráficos por tipo de alerta, usuario y condición
  - Análisis temporal con tendencias
  - KPIs en tiempo real
  - Exportación de gráficos
- **Integración SQL Server**:
  - Conexión configurable (Windows/SQL Authentication)
  - Sincronización bidireccional
  - Backup automático
- **Gestión de Datos**:
  - Importación masiva desde Excel
  - Exportación con formato preservado
  - Visualización tabular con filtros
  - Estadísticas detalladas

## 📋 Requisitos del Sistema

### Dependencias de Python
- Python 3.10 o superior
- PySide6 >= 6.5.0
- pandas >= 2.0.0
- openpyxl >= 3.1.0
- matplotlib >= 3.7.0
- sqlalchemy >= 2.0.0
- pyodbc >= 4.0.39
- bcrypt >= 4.0.0

### Opcional para SQL Server
- Microsoft ODBC Driver 17 for SQL Server
- SQL Server (cualquier versión compatible)

## 🛠️ Instalación

### 1. Clonar o descargar el proyecto
```bash
git clone <url-del-repositorio>
cd BD-alertas
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv .venv
.venv\\Scripts\\activate  # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación
```bash
python main.py
```

## 🔐 Login Inicial

La aplicación incluye un usuario administrador por defecto:
- **Usuario**: `admin`
- **Contraseña**: `admin123`

## 📊 Estructura del Proyecto

```
BD alertas/
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias Python
├── README.md              # Este archivo
├── src/                   # Código fuente
│   ├── gui/              # Interfaz gráfica
│   │   ├── main_window.py        # Ventana principal
│   │   ├── alert_form.py         # Formulario de alertas
│   │   ├── dashboard.py          # Dashboard con gráficos
│   │   ├── data_manager.py       # Gestión de datos
│   │   └── settings_dialog.py    # Configuraciones
│   ├── data/             # Gestión de datos
│   │   ├── excel_manager.py      # Operaciones Excel
│   │   └── sql_manager.py        # Integración SQL Server
│   ├── auth/             # Sistema de autenticación
│   │   └── login_manager.py      # Login y usuarios
│   └── utils/            # Utilidades generales
├── data/                 # Datos de la aplicación
│   └── alertas_geotecnicas.xlsx  # Excel principal (se crea automáticamente)
├── config/               # Configuraciones
│   ├── users.json        # Base de datos de usuarios
│   └── settings.json     # Configuraciones de la app
└── tests/                # Tests unitarios
```

## 💾 Formato de Datos Excel

### Columnas del Archivo Principal

| Columna | Descripción | Tipo |
|---------|-------------|------|
| FechaHora | Fecha y hora del evento | Texto (DD/MM/YYYY HH:MM:SS) |
| TipoAlerta | Amarilla/Naranja/Roja | Texto con color automático |
| Condicion | transgresiva/progresiva/crítica | Texto |
| Respaldo | Ruta del archivo PowerPoint | Texto |
| Colapso | Sí/No | Texto |
| FechaHoraColapso | Fecha del colapso (opcional) | Texto |
| Evacuacion | Sí/No | Texto |
| CronologiaAnalisis | Análisis detallado | Texto largo |
| Observaciones | Observaciones adicionales | Texto largo |
| Usuario | Usuario que registró la alerta | Texto |
| FechaRegistro | Timestamp de registro | Texto |

### Ejemplo de Archivo Excel

La aplicación incluye una función para generar plantillas Excel con ejemplos y formato correcto.

## 🗄️ Configuración SQL Server

### 1. Crear Base de Datos

```sql
CREATE DATABASE AlertasGeotecnicas;
USE AlertasGeotecnicas;
```

### 2. Configurar en la Aplicación

1. Abrir menú **Herramientas > Configuración**
2. Ir a la pestaña **Base de Datos**
3. Configurar:
   - Servidor: `localhost\SQLEXPRESS` (o tu servidor)
   - Base de datos: `AlertasGeotecnicas`
   - Tipo de autenticación
   - Credenciales (si es necesario)

### 3. Probar Conexión

Usar el botón **"Probar Conexión"** en el diálogo de configuración.

## 📈 Uso del Dashboard

### KPIs Disponibles
- **Total de Alertas**: Contador general
- **Alertas Rojas**: Alertas críticas
- **Últimos 30 días**: Alertas recientes
- **Usuarios Activos**: Número de usuarios registrando

### Gráficos Interactivos
- **Distribución por Tipo**: Gráfico de pastel con colores reales
- **Alertas por Usuario**: Top 10 usuarios más activos
- **Distribución por Condición**: Barras comparativas
- **Tendencia Temporal**: Evolución en el tiempo

## 🔧 Configuraciones Avanzadas

### Detección de Duplicados
- Campos configurables para comparación
- Tolerancia en tiempo (minutos)
- Prevención automática de duplicados

### Validaciones
- Campos obligatorios configurables
- Validación de formatos de fecha
- Verificación de archivos de respaldo

### Notificaciones
- Alertas automáticas para alertas rojas
- Configuración de email (futuro)
- Log de actividades

## 🧪 Tests

Ejecutar tests unitarios:

```bash
python -m pytest tests/
```

### Tests Incluidos
- Validación de gestión Excel
- Detección de duplicados
- Operaciones de importación/exportación
- Funciones críticas del sistema

## 🚨 Solución de Problemas

### Error de Conexión SQL Server
1. Verificar que SQL Server esté ejecutándose
2. Instalar Microsoft ODBC Driver 17
3. Verificar permisos de red y firewall
4. Comprobar credenciales de autenticación

### Problemas con Archivos Excel
1. Cerrar Excel si tiene el archivo abierto
2. Verificar permisos de escritura en el directorio
3. Comprobar formato de fechas (DD/MM/YYYY HH:MM:SS)

### Errores de Dependencias
```bash
pip install --upgrade -r requirements.txt
```

## 🔄 Actualizaciones Futuras

### Próximas Funcionalidades
- [ ] Autenticación LDAP/Active Directory
- [ ] Dashboard web con Flask/Streamlit
- [ ] Notificaciones por email/Teams
- [ ] Exportación automática programada
- [ ] API REST para integraciones
- [ ] Análisis predictivo con ML
- [ ] Mapas geoespaciales
- [ ] Reportes PDF automatizados

## 📞 Soporte

Para soporte técnico o reportar problemas:

1. Verificar este README
2. Revisar logs de la aplicación
3. Contactar al equipo de desarrollo

## 📝 Licencia

Este proyecto está desarrollado para uso interno de la organización.

---

**Desarrollado con ❤️ usando Python, PySide6 y tecnologías modernas**
