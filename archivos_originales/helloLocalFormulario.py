# CON LA BASE DE DATOS   LOCAL  BD formulario
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_cors import CORS
# Tipos de metodos:
# GET -> Se utiliza para recuperar informacion del servidor
# POST -> Se utiliza para enviar datos al servidor para su procesamiento
# DELETE -> Se utiliza para eliminar uno o mas recursos en el servidor o BD
# PUT -> Se utiliza para actualizar un recurso en el servidor
# PATCH -> Se utiliza para actualizar parcialmente un recurso en el servidor

# desde aqui habia una conexion con una base de datos postgress local
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/estudiantes_grupo_8'
DATABASE_URL = "postgresql://usuario:contraseña@host:puerto/base_de_datos"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# dhasta aqui habia una conexion con una base de datos postgress local


# Creación del modelo de Formulario (modelo - tabla de la base de datos)
#id, nombre, email, edad
class Formulario(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     nombre = db.Column(db.String(50), nullable = False)
     edad = db.Column(db.Integer, nullable = False)
     email = db.Column(db.String(50), nullable = False)

     def to_dist(self):
         return {
                          'id':self.id, 
                          'nombre':self.nombre, 
                          'edad':self.edad,
                          'email':self.email
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
    return "<p>(hello_local) -    Hello, Big World from Hack_REACT_FLASK_CRUD_AWS!</p>"


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



