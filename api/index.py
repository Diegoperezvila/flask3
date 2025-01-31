from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

uri = 'mongodb+srv://celtadiego:CeltaVigo9@clase.dznbv.mongodb.net/?retryWrites=true&w=majority&appName=Clase'
client = MongoClient(uri)
database = client['Despliegue']
collection = database['PythonAlumnos']

@app.route('/api')
def home():
    return 'Hello, World!'

@app.route('/api/about')
def about():
    return 'About'

@app.route('/api/users/user1', methods=["GET"])
def get_user1():
    return jsonify(collection.find_one({'id': 1}, {'_id': 0}))

@app.route('/api/users', methods=["GET"])
def get_users():
    return jsonify(list(collection.find({}, {'_id': 0})))

@app.route('/api/users', methods=["POST"])
def add_users():
    new_user = request.get_json()
    if 'name' not in new_user:
            return jsonify({"error": "Datos incompletos."}), 400
    
    user_count = collection.count_documents({})
    new_user['id']=user_count+1
    
    collection.insert_one(new_user)
    return jsonify(new_user), 201 #created

@app.route('/api/users/<int:user_id>', methods=["GET"])
def get_userId(user_id):
    userVer = collection.find_one({'id': user_id}, {'_id': 0})
    
    if userVer:
        return jsonify(userVer)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

handle=app