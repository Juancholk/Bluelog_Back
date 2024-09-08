from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }
class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    csv_data = db.Column(db.JSON)  # Cambiado a db.JSON para almacenar datos en formato JSON

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'csv_data': self.csv_data  # El CSV ya estará en formato JSON
        }
