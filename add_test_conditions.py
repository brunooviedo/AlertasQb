"""
Script para agregar datos de prueba con las nuevas condiciones
"""
import sys
sys.path.append('.')

from src.data.excel_manager import ExcelManager
from datetime import datetime

def add_test_data():
    """Agregar datos de prueba con las nuevas condiciones"""
    print("📝 Agregando datos de prueba con nuevas condiciones...")
    
    excel_manager = ExcelManager()
    
    # Datos de prueba con las nuevas condiciones
    test_alerts = [
        {
            "FechaHora": "22/08/2025 14:30:00",
            "TipoAlerta": "Amarilla",
            "Condicion": "Transgresiva-Progresiva",
            "Ubicacion": "Sector A - Prueba",
            "VelocidadMmDia": "2.5",
            "Respaldo": "",
            "Colapso": "No",
            "FechaHoraColapso": "",
            "Evacuacion": "No",
            "CronologiaAnalisis": "Alerta de prueba para nueva condición",
            "Observaciones": "Test de condición Transgresiva-Progresiva",
            "Usuario": "Bruno",
            "FechaRegistro": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "HojaOrigen": "Test"
        },
        {
            "FechaHora": "22/08/2025 15:45:00",
            "TipoAlerta": "Naranja",
            "Condicion": "Progresiva-Crítica",
            "Ubicacion": "Sector B - Prueba",
            "VelocidadMmDia": "4.8",
            "Respaldo": "",
            "Colapso": "No",
            "FechaHoraColapso": "",
            "Evacuacion": "Sí",
            "CronologiaAnalisis": "Alerta de prueba para condición crítica",
            "Observaciones": "Test de condición Progresiva-Crítica",
            "Usuario": "Bruno",
            "FechaRegistro": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "HojaOrigen": "Test"
        }
    ]
    
    # Agregar los datos
    for i, alert_data in enumerate(test_alerts, 1):
        try:
            result = excel_manager.save_alert(alert_data)
            if result:
                print(f"✅ Alerta {i} agregada: {alert_data['Condicion']}")
            else:
                print(f"❌ Error agregando alerta {i}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n🎉 Datos de prueba agregados exitosamente!")
    print("💡 Ahora puedes ver las nuevas condiciones en el dashboard")

if __name__ == "__main__":
    add_test_data()
