import serial
import time

try:
    # Intenta conectar a Bluetooth en el puerto COM5
    BT = serial.Serial('COM6', 115200, timeout=1)
    time.sleep(2)  # Espera un par de segundos para que se establezca la conexión
    print("Connected to BT")
    
    while True:
        mensaje = input("Ingrese un valor 0 o 1: ")
        
        if mensaje in ['0', '1']:
            BT.write(mensaje.encode('utf-8'))
            print(f"Mensaje '{mensaje}' enviado a BT")
        else:
            print("Por favor, ingresa un valor válido (0 o 1)")
        
except serial.SerialException as e:
    print(f"Couldn't connect to BT: {e}")
