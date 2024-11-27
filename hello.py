# desde aqui es el original
# CON LA BASE DE DATOS  AWS  BD formulario
# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import text
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os

# # esto lo sugirio gemini para la conexion aws en vercel
# from sqlalchemy import create_engine

# # esto lo quito si estoy trabajando en vecel, ya esto lo hace vercel
# # load_dotenv()

# app = Flask(__name__) 
# CORS(app)

# db_user = os.getenv('DB_USER')
# db_password = os.getenv('DB_PASSWORD')
# db_host = os.getenv('DB_HOST')
# db_port = os.getenv('DB_PORT')
# db_name = os.getenv('DB_NAME') 

# # Improved connection URL construction
# db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
# app.config['SQLALCHEMY_DATABASE_URI'] = db_url
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# # dhasta aqui habia una conexion con una base de datos postgress local

# # esto lo sugirio gemini para la conexion aws en vercel
# engine = create_engine(db_url)

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text
import os

app = Flask(__name__)
CORS(app)

# Obtener las variables de entorno
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Construir la URL de conexión
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Configurar SQLAlchemy con opciones adicionales
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False  # Desactivar las consultas SQL en la consola
app.config['SQLALCHEMY_POOL_SIZE'] = 20  # Ajustar el tamaño del pool de conexiones
db = SQLAlchemy(app)

# Función para manejar errores de conexión a la base de datos
def handle_db_error(error):
    # Puedes personalizar este manejador para enviar notificaciones, registrar errores, etc.
    print(f"Error de conexión a la base de datos: {error}")
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

#
# ... Resto de tu código


# Creación del modelo de Formulario (modelo - tabla de la base de datos)
#id, nombre, email, edad
class Formulario(db.Model):
     nombre = db.Column(db.String(50), nullable = False)
     email = db.Column(db.String(50), nullable = False)
     edad = db.Column(db.Integer, nullable = False)
     id = db.Column(db.Integer, primary_key = True)
    
     def to_dist(self):
         return {
                          'nombre':self.nombre, 
                          'email':self.email,
                          'edad':self.edad,
                          'id':self.id
         }

# Creación de la Base de Dato y su tabla
with app.app_context():
     db.create_all()

#Verificar la conexion a la base de datos
     try:  
        #  #Realizamos una consulta simple
        db.session.execute(text('SELECT 1'))
        print("Conexion a la base de datos exitosa")
     except Exception as e:
        print(f'Error al conectar a la base de datos: {e}')

@app.route("/")
def hello_world():
    return "<p>(hello_AWS) -    Hello desde Vercel, Big World from Hack_REACT_FLASK_CRUD_AWS!</p>"


# POST -> Se utiliza para enviar datos al servidor para su procesamiento
# Ruta para crear un estudiante.
@app.route('/create-formulario', methods=['POST'])
def create_formulario():
    data = request.json
    new_formulario =Formulario(nombre = data['nombre'],
                          edad = data['edad'],
                          email = data['email'] ) 
    db.session.add(new_formulario)
    db.session.commit()
    return jsonify({'message': 'Usuario creado correctamente', 
                    'data': new_formulario.to_dist()})

# GET -> Se utiliza para recuperar informacion del servidor
@app.route('/formularios', methods=['GET'])
def get_formularios():
    formularios = Formulario.query.all()
    return jsonify([formulario.to_dist() for formulario in formularios])

# #  Ruta para obtener un usuario por params ( Por parametro de ruta )
@app.route('/formularios/<int:formulario_id>', methods=['GET'])
def get_formulario_by_id(formulario_id):
    formulario = Formulario.query.get(formulario_id)
    if formulario:
           return jsonify(formulario.to_dist())
    return jsonify({'message': 'El usuario no ha sido encontrado'})
    

# # AQUI Ruta para actualizar parcialmente un usuario
@app.route('/patch-formulario/<int:formulario_id>', methods=['PATCH'])
def update_one_formulario(formulario_id):
    data = request.json
    formulario = Formulario.query.get(formulario_id)
    if formulario:
       for key, value in data.items():
           setattr(formulario, key, value)
       db.session.commit()
       return jsonify({'message': 'Usuario actualizado parcialmente', 'data': formulario.to_dist()})
    return jsonify({'message': 'Usuario actualizado parcialmente'})

# # Ruta para eliminar un usuario por query params
@app.route('/delete-formulario/<int:formulario_id>', methods=['DELETE'])
def delete_formulario_by_nombre(formulario_id):
    formulario = Formulario.query.get(formulario_id)

    if formulario:
        db.session.delete(formulario)
        db.session.commit()
        return jsonify({'message': f'Usuario con ID {formulario_id} eliminado'})
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404



