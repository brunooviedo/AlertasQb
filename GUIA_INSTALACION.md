# 📥 AlertasQB - Guía de Instalación

¡Bienvenido al **Sistema de Alertas Geotécnicas**! 🛡️

## 🚀 Opciones de Instalación

### 🎯 **Opción 1: Ejecutable Independiente (RECOMENDADO)**

**✅ Más fácil - Solo descargar y ejecutar**

1. **Descargar:**
   - Ve a: https://github.com/brunooviedo/AlertasQb/releases/latest
   - Descarga: `AlertasQB-Standalone-v1.2.1.zip` (85 MB)

2. **Instalar:**
   - Extrae el ZIP en cualquier carpeta (ej: `C:\AlertasQB`)
   - Ejecuta `AlertasQB.exe`
   - ¡Listo! 🎉

**Características:**
- ✅ No requiere Python
- ✅ No requiere instalación
- ✅ Incluye todas las dependencias
- ✅ Actualizaciones automáticas
- ✅ Solo 85 MB

---

### 🔧 **Opción 2: Código Fuente (Para Desarrolladores)**

**Para usuarios avanzados que quieren modificar el código**

1. **Descargar:**
   - Descarga: `AlertasQB-v1.2.1.zip` (código fuente)

2. **Instalar Python:** (si no lo tienes)
   ```bash
   winget install Python.Python.3.12
   ```

3. **Instalación automática:**
   - Extrae el ZIP
   - Ejecuta `instalar.bat` 
   - O sigue los pasos manuales:

4. **Instalación manual:**
   ```bash
   # Crear entorno virtual
   python -m venv .venv
   
   # Activar entorno
   .venv\Scripts\Activate.ps1
   
   # Instalar dependencias
   pip install -r requirements.txt
   
   # Ejecutar
   python main.py
   ```

---

## 🖥️ **Requisitos del Sistema**

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| **OS** | Windows 10 | Windows 11 |
| **RAM** | 4 GB | 8 GB |
| **Disco** | 500 MB | 1 GB |
| **Resolución** | 1024x768 | 1920x1080 |

---

## 🔧 **Funciones Incluidas**

- 📊 **Dashboard interactivo** con gráficos en tiempo real
- 🔐 **Sistema de usuarios** con autenticación
- 📁 **Gestión de datos** Excel integrada  
- 🔄 **Actualizaciones automáticas** desde GitHub
- 📈 **Reportes y estadísticas** avanzadas
- 💾 **Respaldos automáticos** de datos
- 🎨 **Interfaz moderna** con PySide6

---

## 🆘 **Soporte y Ayuda**

### 📧 **Contacto:**
- **Email**: bruno@alertasqb.com
- **GitHub**: https://github.com/brunooviedo/AlertasQb

### 🐛 **Reportar Problemas:**
- **Issues**: https://github.com/brunooviedo/AlertasQb/issues/new
- **Incluye**: Versión de Windows, descripción del error, captura de pantalla

### 📖 **Documentación:**
- **Manual completo**: https://github.com/brunooviedo/AlertasQb/blob/main/README.md
- **Actualizaciones**: https://github.com/brunooviedo/AlertasQb/blob/main/SISTEMA_ACTUALIZACION.md

---

## 🔄 **Actualizaciones**

AlertasQB se actualiza automáticamente:
- ✅ **Verificación al inicio** de la aplicación
- ✅ **Descarga automática** de nuevas versiones
- ✅ **Instalación sin perder datos** (config y datos protegidos)
- ✅ **Respaldos automáticos** antes de cada actualización

---

## 🎉 **¡Disfruta AlertasQB!**

Después de la instalación:
1. 🔐 **Inicia sesión** con tu usuario
2. 📊 **Explora el dashboard** con tus datos
3. 📁 **Gestiona alertas** desde la interfaz
4. ⚙️ **Configura opciones** según tus necesidades

**¡Tu sistema de alertas geotécnicas está listo!** 🛡️
