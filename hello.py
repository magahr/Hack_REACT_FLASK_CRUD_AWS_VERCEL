from flask import Flask, jsonify, request

# Tipos de metodos:
# GET -> Se utiliza para recuperar informacion del servidor
# POST -> Se utiliza para enviar datos al servidor para su procesamiento
# DELETE -> Se utiliza para eliminar uno o mas recursos en el servidor o BD
# PUT -> Se utiliza para actualizar un recurso en el servidor
# PATCH -> Se utiliza para actualizar parcialmente un recurso en el servidor

app = Flask(__name__)

students = [
    {
        "name": 'Adrian',
        "age": 31,
        "major": "Computer Science"
    },
    {
        "name": 'Hiram',
        "age": 23,
        "major": "Computer Science"
    },
    {
        "name": 'Andres',
        "age": 27,
        "major": "Computer Science"
    },
    {
        "name": 'Keishmer',
        "age": 22,
        "major": "Computer Science"
    }
]

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/oplesk', methods=['GET','POST','DELETE','PUT','PATCH'])
def social_oplesk():
    return '<h1> Hello; from oplesk </h1>'


#  Ruta para obtener estudiantes
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

# Ruta para crear un estudiante.

@app.route('/create-student', methods=['POST'])
def create_student():
    data = request.json
    students.append(data)
    
    return jsonify({'message': 'Estudiante creado correctamente', 'data': data})
    