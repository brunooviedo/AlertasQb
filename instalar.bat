@echo off
echo ====================================
echo     INSTALADOR AlertasQB v1.2.1
echo ====================================
echo.

echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Instalando...
    winget install Python.Python.3.12
    if errorlevel 1 (
        echo ❌ Error instalando Python. Instálalo manualmente desde python.org
        pause
        exit /b 1
    )
    echo ✅ Python instalado
) else (
    echo ✅ Python encontrado
)

echo.
echo [2/5] Creando entorno virtual...
if not exist ".venv" (
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Error creando entorno virtual
        pause
        exit /b 1
    )
    echo ✅ Entorno virtual creado
) else (
    echo ✅ Entorno virtual ya existe
)

echo.
echo [3/5] Activando entorno virtual...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Error activando entorno virtual
    pause
    exit /b 1
)
echo ✅ Entorno virtual activado

echo.
echo [4/5] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)
echo ✅ Dependencias instaladas

echo.
echo [5/5] Creando acceso directo...
echo @echo off > "Ejecutar AlertasQB.bat"
echo cd /d "%~dp0" >> "Ejecutar AlertasQB.bat"
echo call .venv\Scripts\activate.bat >> "Ejecutar AlertasQB.bat"
echo python main.py >> "Ejecutar AlertasQB.bat"
echo pause >> "Ejecutar AlertasQB.bat"
echo ✅ Acceso directo creado

echo.
echo ====================================
echo    🎉 INSTALACIÓN COMPLETADA
echo ====================================
echo.
echo Para ejecutar AlertasQB:
echo 1. Doble clic en "Ejecutar AlertasQB.bat"
echo 2. O ejecuta: python main.py
echo.
echo 📧 Soporte: bruno@alertasqb.com
echo 🌐 Web: https://github.com/brunooviedo/AlertasQb
echo.
pause
