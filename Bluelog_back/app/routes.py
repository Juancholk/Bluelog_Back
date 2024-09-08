from flask import Blueprint, request, jsonify
from .models import db, User
from bluetooth_comm import send_bluetooth_message
from estadisticos import generate_statistics
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

# Crear un nuevo usuario
@main.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# Actualizar un usuario
@main.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    user.username = data.get('username', user.username)
    db.session.commit()
    
    return jsonify(user.to_dict())

# Eliminar un usuario
@main.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 204

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

