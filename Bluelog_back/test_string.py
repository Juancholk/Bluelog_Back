import serial


BT = serial.Serial('COM5', 115200)
print("Connected to BT")

print("Couldn't connect to BT")
while True:
    mensaje = input("Ingrese un valor 0 o 1: ")
    BT.write(mensaje.encode('utf-8'))