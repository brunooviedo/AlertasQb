# 📥 Cómo instalar AlertasQB

## 🚀 Instalación rápida

### Método 1: Descarga desde GitHub

1. **Descargar la aplicación:**
   - Ve a: https://github.com/brunooviedo/AlertasQb/releases/latest
   - Descarga el archivo `AlertasQB-v1.2.1.zip`

2. **Extraer e instalar:**
   ```bash
   # Extrae el ZIP en una carpeta (ej: C:\AlertasQB)
   # Abre PowerShell en esa carpeta y ejecuta:
   
   # Instalar Python (si no lo tienes)
   winget install Python.Python.3.12
   
   # Crear entorno virtual
   python -m venv .venv
   
   # Activar entorno
   .\.venv\Scripts\Activate.ps1
   
   # Instalar dependencias
   pip install -r requirements.txt
   
   # Ejecutar aplicación
   python main.py
   ```

3. **¡Listo!** La aplicación se ejecutará con todas las funciones.

### Método 2: Ejecutable independiente (Próximamente)

- Descargar un solo archivo .exe
- Doble clic para ejecutar
- No requiere instalación de Python

## 🔧 Requisitos del sistema

- **Windows 10/11** (recomendado)
- **Python 3.10+** (se instala automáticamente)
- **4 GB RAM** mínimo
- **500 MB** espacio libre

## 🆘 Soporte

- **Email**: bruno@alertasqb.com
- **Issues**: https://github.com/brunooviedo/AlertasQb/issues
- **Documentación**: https://github.com/brunooviedo/AlertasQb/blob/main/README.md

## 🔄 Actualizaciones automáticas

La aplicación se actualiza automáticamente:
- ✅ Verificación al inicio
- ✅ Descarga automática
- ✅ Instalación sin perder datos
- ✅ Respaldos automáticos
