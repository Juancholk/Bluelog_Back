from flask import Blueprint, request, jsonify, render_template, send_from_directory
from .models import db, User, Folder
from bluetooth_comm import send_bluetooth_message
from estadisticos import generate_statistics
from werkzeug.utils import secure_filename
import os
import csv
from io import StringIO

main = Blueprint('main', __name__)

# Ruta de prueba
@main.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to Flask API"})

# Obtener todos los usuarios
@main.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


#Obtener json de un formulario
@main.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.get_json()
    frecuency = data.get('frecuency')
    muestreo = data.get('muestreo')
    periodo = data.get('periodo')

    # Preparar un mensaje para enviar al microcontrolador
    message = f"{frecuency},{muestreo},{periodo}"

    # Llamar a la función para enviar el mensaje por Bluetooth
    bt_response = send_bluetooth_message(message)

    return jsonify({
        'message': 'Formulario recibido y procesado',
        'bluetooth_status': bt_response
    })

@main.route('/estadistics', methods=['POST'])
def calculate_statistics():
    try:
        # Llamar a la función para generar estadísticas
        statistics = generate_statistics()
        return jsonify(statistics), 200
    
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 500
    except Exception as e:
        #app.logger.error(f"Error generating statistics: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    
@main.route('/upload_csv/<int:folder_id>', methods=['POST'])
def upload_csv(folder_id):
    try:
        # Obtener el archivo CSV desde la solicitud
        file = request.files['file']
        
        # Leer el contenido del archivo CSV
        stream = StringIO(file.stream.read().decode('UTF-8'))
        csv_reader = csv.DictReader(stream)

        # Convertir el CSV en una lista de diccionarios (JSON)
        csv_content = [row for row in csv_reader]

        # Buscar el Folder por ID y almacenar el JSON directamente
        folder = Folder.query.get(folder_id)
        if folder:
            folder.csv_data = csv_content  # No hace falta convertirlo, ya es JSON
            db.session.commit()
            return jsonify({'message': 'CSV uploaded and stored as JSON in folder'}), 200
        else:
            return jsonify({'error': 'Folder not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@main.route('/get_csv/<int:folder_id>', methods=['GET'])
def get_csv(folder_id):
    folder = Folder.query.get(folder_id)
    if folder and folder.csv_data:
        return jsonify({'csv_data': folder.csv_data}), 200  # No hace falta hacer json.loads
    else:
        return jsonify({'error': 'Folder or CSV not found'}), 404

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        return jsonify({
            "message": "Login successful", 
            "status": "success",
            "user_id": user.id  # Incluye el ID del usuario en la respuesta
        })
    else:
        return jsonify({"message": "Invalid credentials", "status": "fail"}), 401


@main.route('/folders/<int:user_id>', methods=['GET'])
def get_folders(user_id):
    folders = Folder.query.filter_by(user_id=user_id).all()
    folder_list = [{
        'id': folder.id,
        'name': folder.name,
        'user_id': folder.user_id,
        'csv_data': folder.csv_data,
        'image_path': f'/imagenes/{folder.image_path}'  # Construye la URL relativa
    } for folder in folders]
    return jsonify(folder_list), 200

@main.route('/folders', methods=['POST'])
def create_folder():
    data = request.form  # Obtén los datos del formulario (excepto el archivo)

    new_folder = Folder(
        name=data['name'],
        user_id=data['user_id'],
        csv_data=data['csv_data']
    )
    db.session.add(new_folder)
    db.session.commit()
    return jsonify(new_folder.to_dict()), 201

# Eliminar una carpeta
@main.route('/folders/<int:folder_id>', methods=['DELETE'])
def delete_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    db.session.delete(folder)
    db.session.commit()
    return '', 204  # 204 No Content