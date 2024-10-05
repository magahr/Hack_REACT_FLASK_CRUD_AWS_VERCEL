from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Tipos de metodos:
# GET -> Se utiliza para recuperar informacion del servidor
# POST -> Se utiliza para enviar datos al servidor para su procesamiento
# DELETE -> Se utiliza para eliminar uno o mas recursos en el servidor o BD
# PUT -> Se utiliza para actualizar un recurso en el servidor
# PATCH -> Se utiliza para actualizar parcialmente un recurso en el servidor



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/estudiantes_grupo_8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Creación del modelo de Student (modelo - tabla de la base de datos)
class Student(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     name = db.Column(db.String(50), nullable = False)
     age = db.Column(db.Integer, nullable = False)
     major = db.Column(db.String(50), nullable = False)

     def to_dist(self):
         return {
                          'id':self.id, 
                          'name':self.name, 
                          'age':self.age,
                          'major':self.major
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
    return "<p>Hello, World from flask-grupo-8-profe!</p>"

# #  Ruta para obtener estudiantes  en el minuto 14:45 - esto se hizo con un dictionary
# @app.route('/students', methods=['GET'])
# def get_students():
#     return jsonify(students)


# POST -> Se utiliza para enviar datos al servidor para su procesamiento
# Ruta para crear un estudiante.
@app.route('/create-student', methods=['POST'])
def create_student():
    data = request.json
    new_student = Student(name = data['name'],
                          age = data['age'],
                          major = data['major'] ) 
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Estudiante creado correctamente', 
                    'data': new_student.to_dist()})

# GET -> Se utiliza para recuperar informacion del servidor
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dist() for student in students])

# #  Ruta para obtener un estudiante por params ( Por parametro de ruta )
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    student = Student.query.get(student_id)
    if student:
           return jsonify(student.to_dist())
    return jsonify({'message': 'El estudiante no ha sido encontrado'})
    

# Ruta para borrar todos los estudiantes
@app.route('/delete-students', methods=['DELETE'])
def delete_all_students():
    db.session.query(Student).delete()
    db.session.commit()
    return jsonify({'message': 'Estudiantes borrados correctamente'})

# # AQUI Ruta para actualizar parcialmente un estudiante
@app.route('/patch-student/<int:student_id>', methods=['PATCH'])
def update_one_student(student_id):
    data = request.json
    student = Student.query.get(student_id)
    if student:
       for key, value in data.items():
           setattr(student, key, value)
       db.session.commit()
       return jsonify({'message': 'Estudiante actualizado parcialmente', 'data': student.to_dist()})
    return jsonify({'message': 'Estudiante actualizado parcialmente'})

# # Ruta para eliminar un estudiante por query params
@app.route('/delete-student/', methods=['DELETE'])
def delete_student_by_name():
     name = request.args.get('name')
     student = Student.query.filter_by(name=name).first()
     if student:
          db.session.delete(student)
          db.session.commit()
          return jsonify({'message': f'Estudiante {name} eliminado'})
     return jsonify({'message': 'Estudiante no encontrado'})
    








# @app.route('/students', methods=['GET'])
# def get_students():
#     students = Student.query.all()
#     return jsonify([{'id':student.id, 
#                       'name':student.name, 
#                       'age':student.age,
#                       'major':student.major} for student in students])

# @app.route('/')
# def hello_world():
#     return 'Hello, EveryBody!'

# @app.route('/oplesk', methods=['GET','POST','DELETE','PUT','PATCH'])
# def social_oplesk():
#     return '<h1> Hello; from oplesk </h1>'


# #  Ruta para obtener estudiantes
# @app.route('/students', methods=['GET'])
# def get_students():
#     return jsonify(students)

# #  Ruta para obtener un estudiante por params ( Por parametro de ruta )
# @app.route('/students/<int:student_id>', methods=['GET'])
# def get_student_by_id(student_id):
#     for student in students:
#         if student.get('id') == student_id:
#             return jsonify(student)
#     return jsonify({'message': 'El estudiante no ha sido encontrado'})
    

# # Ruta para crear un estudiante.
# @app.route('/create-student', methods=['POST'])
# def create_student():
#     data = request.json
#     students.append(data)
#     return jsonify({'message': 'Estudiante creado correctamente', 'data': data})

# # Ruta para borrar todos los estudiantes
# @app.route('/delete-students', methods=['DELETE'])
# def delete_all_students():
#     students.clear()
#     return jsonify({'message': 'Estudiantes borrados correctamente'})

# # Ruta para actualizar parcialmente un estudiante
# @app.route('/patch-student', methods=['PATCH'])
# def update_one_student():
#     data = request.json
#     students[0].update(data) # Actualiza el priomer estudiante de la lista.
#     return jsonify({'message': 'Estudiante actualizado parcialmente'})

# # Ruta para eliminar un estudiante por query params
# @app.route('/delete-student/', methods=['DELETE'])
# def delete_student_by_name():
#     name = request.args.get('name')
#     if name:
#         for student in students:
#             if student.get('name') == name:
#                 students.remove(student)
#                 return jsonify({'message': f'Estudiante {name} eliminado'})
#         return jsonify({'message': 'Estudiante no encontrado'})
#     return jsonify({'message': 'Proporciona un nombre de estudiante'})