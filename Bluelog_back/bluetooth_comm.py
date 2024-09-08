# bluetooth_comm.py
import serial
import json

def send_bluetooth_message(message):
    try:
        BT = serial.Serial('COM5', 115200)  # Ajusta el puerto y la velocidad según tu configuración
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
        #print("JSON sent:", json_data_str)
        
        # Enviar el mensaje JSON al microcontrolador
        BT.write(json_data_str.encode('utf-8'))
        #print("Message sent ", json_data_str.encode('utf-8'))
        
        # Cerrar la conexión
        BT.close()
        return "Mensaje enviado correctamente"
    except Exception as e:
        print("Couldn't connect to BT")
        return str(e)

