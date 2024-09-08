import serial
import json

def test_serial_connection():
    try:
        # Crear el objeto JSON
        data = {
            "frecuency": 2000,
            "muestreo": 500,
            "periodo": 10
        }

        # Convertir el objeto JSON a una cadena
        json_data = json.dumps(data) + "\n"  # Agregar un salto de línea al final
        print("JSON data:", json_data)
        # Conectar al puerto serial
        BT = serial.Serial('COM5', 115200)
        print("Connected to BT")

        # Enviar la cadena JSON codificada en UTF-8
        BT.write(json_data.encode('utf-8'))
        print("JSON sent:", json_data)

        # Cerrar la conexión serial
        BT.close()
    except Exception as e:
        print("Couldn't connect to BT:", e)

test_serial_connection()
