from . import db
import base64
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password':self.password
        }
class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    csv_data = db.Column(db.JSON, nullable=True)
    image_path = db.Column(db.String(255), nullable=True)  # Nueva columna para almacenar la ruta de la imagen

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'csv_data': self.csv_data,
            'image_path': self.image_path  # Devuelve la ruta de la imagen
        }


