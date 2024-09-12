from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy()
migrate = Migrate() 
def create_app():
    app = Flask(__name__, static_folder='app/imagenes')
    
    # Configuración de la base de datos
    app.config.from_object('config.Config')

    # Inicializa la base de datos
    db.init_app(app)
    
    # Inicializa Flask-Migrate
    migrate.init_app(app, db)
    
    # Importa las rutas
    from .routes import main
    app.register_blueprint(main, url_prefix='/')  # Registra el blueprint con el prefijo de URL '/'

    return app
