from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from bson import ObjectId

# Instantiation
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://Exam:123@cluster0.bpqynxd.mongodb.net/Proy?retryWrites=true&w=majority&appName=Cluster0'
mongo = PyMongo(app)

# Settings
CORS(app)

# Database
db = mongo.db.bunuelos
db.find()
# Routes
@app.route('/products', methods=['POST'])
def createProduct():
    print(request.json)
    product = {
        'sabor': request.json.get('sabor', ''),
        'cantidad': request.json.get('cantidad', 0),
        'tamano': request.json.get('tamano', ''),
        'precio': request.json.get('precio', ''),
        'imagen': request.json.get('imagen', ''),
        'temperatura': request.json.get('temperatura', 0),
        'nombre': request.json.get('nombre', ''),
        'descripcion': request.json.get('descripcion', ''),
        'fecha_elaboracion': request.json.get('fecha_elaboracion', ''),
        'ubicacion': request.json.get('ubicacion', ''),
        'ingredientes': request.json.get('ingredientes', []),
        'mensaje': request.json.get('mensaje', '')
    }
    result = db.insert_one(product)
    print("llega")
    return jsonify(str(result.inserted_id)), 201


@app.route('/products', methods=['GET'])
def getProducts():
    products = []
    for doc in db.find():
        products.append({
            '_id': str(ObjectId(doc['_id'])),
            'sabor': doc.get('sabor', ''),
            'cantidad': doc.get('cantidad', 0),
            'tamano': doc.get('tamano', ''),
            'precio': doc.get('precio', ''),
            'imagen': doc.get('imagen', ''),
            'temperatura': doc.get('temperatura', 0),
            'nombre': doc.get('nombre', ''),
            'descripcion': doc.get('descripcion', ''),
            'fecha_elaboracion': doc.get('fecha_elaboracion', ''),
            'ubicacion': doc.get('ubicacion', ''),
            'ingredientes': doc.get('ingredientes', []),
            'mensaje': doc.get('mensaje', '')
        })
    return jsonify(products)


@app.route('/products/<id>', methods=['GET'])
def getProduct(id):
    product = db.find_one({'_id': id})
    
    if product:
        print(product)
        return jsonify({
            '_id': str(ObjectId(product['_id'])),
            'sabor': product.get('sabor', ''),
            'cantidad': product.get('cantidad', 0),
            'tamano': product.get('tamano', ''),
            'precio': product.get('precio', ''),
            'imagen': product.get('imagen', ''),
            'temperatura': product.get('temperatura', 0),
            'nombre': product.get('nombre', ''),
            'descripcion': product.get('descripcion', ''),
            'fecha_elaboracion': product.get('fecha_elaboracion', ''),
            'ubicacion': product.get('ubicacion', ''),
            'ingredientes': product.get('ingredientes', []),
            'mensaje': product.get('mensaje', '')
        })
    else:
        return jsonify({'error': 'Product not found'}), 404


@app.route('/products/<id>', methods=['DELETE'])
def deleteProduct(id):
    result = db.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'Product Deleted'})
    else:
        return jsonify({'error': 'Product not found'}), 404


@app.route('/products/<id>', methods=['PUT'])
def updateProduct(id):
    print(request.json)
    update_data = {
        'sabor': request.json.get('sabor', ''),
        'cantidad': request.json.get('cantidad', 0),
        'tamano': request.json.get('tamano', ''),
        'precio': request.json.get('precio', ''),
        'imagen': request.json.get('imagen', ''),
        'temperatura': request.json.get('temperatura', 0),
        'nombre': request.json.get('nombre', ''),
        'descripcion': request.json.get('descripcion', ''),
        'fecha_elaboracion': request.json.get('fecha_elaboracion', ''),
        'ubicacion': request.json.get('ubicacion', ''),
        'ingredientes': request.json.get('ingredientes', []),
        'mensaje': request.json.get('mensaje', '')
    }
    if isinstance(id, str):
        id = ObjectId(id)
    result = db.update_one({'_id': ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 1:
        return jsonify({'message': 'Product Updated'})
    else:
        return jsonify({'error': 'Product not found'}), 404


if __name__ == "__main__":
    app.run(debug=True)
