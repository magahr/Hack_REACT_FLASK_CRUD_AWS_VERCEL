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
        "id": 1,
        "name": 'Adrian',
        "age": 31,
        "major": "Computer Science"
    },
    {
        "id": 2,
        "name": 'Hiram',
        "age": 23,
        "major": "Computer Science"
    },
    {
        "id": 3,
        "name": 'Andres',
        "age": 27,
        "major": "Computer Science"
    },
    {
        "id": 4,
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

#  Ruta para obtener un estudiante por params ( Por parametro de ruta )
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    for student in students:
        if student.get('id') == student_id:
            return jsonify(student)
    return jsonify({'message': 'El estudiante no ha sido encontrado'})
    

# Ruta para crear un estudiante.
@app.route('/create-student', methods=['POST'])
def create_student():
    data = request.json
    students.append(data)
    return jsonify({'message': 'Estudiante creado correctamente', 'data': data})

# Ruta para borrar todos los estudiantes
@app.route('/delete-students', methods=['DELETE'])
def delete_all_students():
    students.clear()
    return jsonify({'message': 'Estudiantes borrados correctamente'})

# Ruta para actualizar parcialmente un estudiante
@app.route('/patch-student', methods=['PATCH'])
def update_one_student():
    data = request.json
    students[0].update(data) # Actualiza el priomer estudiante de la lista.
    return jsonify({'message': 'Estudiante actualizado parcialmente'})

# Ruta para eliminar un estudiante por query params
@app.route('/delete-student/', methods=['DELETE'])
def delete_student_by_name():
    name = request.args.get('name')
    if name:
        for student in students:
            if student.get('name') == name:
                students.remove(student)
                return jsonify({'message': f'Estudiante {name} eliminado'})
        return jsonify({'message': 'Estudiante no encontrado'})
    return jsonify({'message': 'Proporciona un nombre de estudiante'})