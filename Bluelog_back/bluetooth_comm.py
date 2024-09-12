# bluetooth_comm.py
import serial
import json
import time

def send_bluetooth_message(message):
    BT = None  # Variable para almacenar la conexión serial
    try:
        # Conexión al puerto COM5
        BT = serial.Serial('COM6', 115200, timeout=1)  # Ajusta el puerto y la velocidad según tu configuración
        print("Connected to BT")
        
        # Dividir el mensaje en partes
        message = message.split(",")
        
        # Crear un objeto JSON a partir de los valores
        json_data = {
            "frecuency": message[0],
            "muestreo": message[1],
            "periodo": message[2]
        }
        
        # Convertir el objeto JSON a una cadena con formato JSON
        json_data_str = json.dumps(json_data) + "\n"  # Agregar un salto de línea al final para que el ESP32 lo detecte
        
        # Mostrar el JSON que se enviará
        print("JSON sent:", json_data_str)
        
        # Enviar el mensaje JSON al microcontrolador
        BT.write(json_data_str.encode('utf-8'))
        
        # Esperar un breve momento para asegurar que los datos se envíen antes de cerrar
        time.sleep(1)
        
        return "Mensaje enviado correctamente"
    except Exception as e:
        print("Couldn't connect to BT:", str(e))
        return str(e)
    finally:
        # Cerrar la conexión si está abierta
        if BT is not None and BT.is_open:
            BT.close()
            print("BT connection closed")
