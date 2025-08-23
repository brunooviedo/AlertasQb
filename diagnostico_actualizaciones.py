#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico del sistema de actualizaciones
"""

import sys
import os
import json
import requests
from pathlib import Path

# Añadir el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from utils.version import APP_VERSION, UPDATE_SERVER_URL
    from utils.updater import UpdateChecker
    print(f"✅ Módulos importados correctamente")
    print(f"📋 Versión actual: {APP_VERSION}")
    print(f"🌐 URL del servidor: {UPDATE_SERVER_URL}")
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1)

def test_internet_connection():
    """Prueba la conexión a internet"""
    try:
        print("\n🌐 Probando conexión a internet...")
        response = requests.get("https://google.com", timeout=5)
        print(f"✅ Conexión a internet: OK (status: {response.status_code})")
        return True
    except Exception as e:
        print(f"❌ Sin conexión a internet: {e}")
        return False

def test_github_api():
    """Prueba la API de GitHub"""
    try:
        print("\n🔍 Probando API de GitHub...")
        response = requests.get(UPDATE_SERVER_URL, timeout=10)
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            latest_version = data.get('tag_name', '').replace('v', '')
            print(f"📋 Versión en GitHub: {latest_version}")
            print(f"📦 Archivos disponibles: {len(data.get('assets', []))}")
            
            # Mostrar assets
            for asset in data.get('assets', []):
                print(f"   - {asset['name']} ({asset['size']} bytes)")
            
            return data
        else:
            print(f"❌ Error en API: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error conectando con GitHub: {e}")
        return None

def test_update_checker():
    """Prueba el UpdateChecker"""
    try:
        print(f"\n🔄 Probando UpdateChecker...")
        checker = UpdateChecker(UPDATE_SERVER_URL, APP_VERSION)
        result = checker.check_for_updates()
        print(f"📋 Resultado del check: {result}")
        return True
    except Exception as e:
        print(f"❌ Error en UpdateChecker: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🔧 DIAGNÓSTICO SISTEMA DE ACTUALIZACIONES")
    print("=" * 60)
    
    # Test 1: Conexión a internet
    if not test_internet_connection():
        print("\n❌ Sin conexión a internet. El sistema de actualizaciones no funcionará.")
        return
    
    # Test 2: API de GitHub
    github_data = test_github_api()
    if not github_data:
        print("\n❌ No se puede acceder a la API de GitHub.")
        return
    
    # Test 3: UpdateChecker
    test_update_checker()
    
    # Test 4: Comparación de versiones
    print(f"\n📊 COMPARACIÓN DE VERSIONES:")
    current = APP_VERSION
    latest = github_data.get('tag_name', '').replace('v', '')
    
    print(f"   📍 Versión actual: {current}")
    print(f"   📍 Versión GitHub: {latest}")
    
    if current == latest:
        print("   ✅ Versiones iguales - No hay actualización")
    elif current < latest:
        print("   🆕 Hay actualización disponible")
    else:
        print("   ⚠️  Versión local más nueva que GitHub")
    
    print("\n" + "=" * 60)
    print("✅ DIAGNÓSTICO COMPLETADO")
    print("=" * 60)

if __name__ == "__main__":
    main()
