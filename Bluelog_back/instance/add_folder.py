import sqlite3
import os

# Ruta absoluta al archivo de la base de datos
db_path = r'C:\Users\juanc\OneDrive\Documentos\GitHub\Bluelog_Backend\Bluelog_back\instance\mydatabase.db'

# Ruta a la carpeta de las imágenes
image_folder_path = r'C:\Users\juanc\OneDrive\Documentos\GitHub\Bluelog_Backend\Bluelog_back\app\imagenes'

# Rutas a las imágenes específicas
image1 = os.path.join(image_folder_path, 'paisaje.jpg')
image2 = os.path.join(image_folder_path, 'paisaje.jpg')  # Reutilizando la misma imagen

# Conectar a la base de datos SQLite
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Datos de ejemplo para agregar, incluyendo la ruta de la imagen en lugar de los datos binarios
    folders = [
        {'name': 'Cartagena', 'user_id': 1, 'csv_data': '{}', 'image_path': image1},
        {'name': 'Tumaco', 'user_id': 1, 'csv_data': '{}', 'image_path': image2}
    ]

    # Insertar los datos en la tabla Folder
    for folder in folders:
        cursor.execute('''
            INSERT INTO folder (name, user_id, csv_data, image_path)
            VALUES (?, ?, ?, ?)
        ''', (folder['name'], folder['user_id'], folder['csv_data'], folder['image_path']))

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    print("Datos agregados correctamente.")
except sqlite3.Error as e:
    print(f"Error al conectar o ejecutar en la base de datos: {e}")
finally:
    conn.close()
