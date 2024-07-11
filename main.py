from flask import Flask, request, jsonify, render_template # type: ignore
from pymongo import MongoClient # type: ignore
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME
from bson.objectid import ObjectId # type: ignore

app = Flask('__name__')
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

@app.route('/')
def index():
    return render_template('index.html')

new_appart = {"id_mutation":"new_id",
  "date_mutation":"2024-07-10",
  "nature_mutation":"Vente",
  "valeur_fonciere":226700,
  "adresse_numero":173,
  "adresse_nom_voie":"CHE DU MOULIN DE POLAIZE",
  "adresse_code_voie":"164",
  "code_postal":1310
}

@app.route('/add', methods=['POST'])
def add_property():
    property_data = request.json
    if not property_data:
        return jsonify({"status": "Failed", "message": "No data provided"}), 400
    try:
        collection.insert_one(property_data)
        return jsonify({"status": "Property added"}), 201
    except Exception as e:
        return jsonify({"status": "Failed", "message": str(e)}), 500
    
collection.insert_one(new_appart)

@app.route('/properties', methods=['GET'])
def get_properties():
    properties = list(collection.find())
    for property in properties:
        property["_id"] = str(property["_id"])
    return jsonify(properties)

@app.route('/update/<property_id>', methods=['PUT'])
def update_property(property_id):
    property_data = request.json
    try:
        collection.update_one({"_id": ObjectId(property_id)}, {"$set": property_data})
        return jsonify({"status": "Property updated"}), 200
    except Exception as e:
        return jsonify({"status": "Failed", "message": str(e)}), 500

@app.route('/delete/<property_id>', methods=['DELETE'])
def delete_property(property_id):
    try:
        collection.delete_one({"_id": ObjectId(property_id)})
        return jsonify({"status": "Property deleted"}), 200
    except Exception as e:
        return jsonify({"status": "Failed", "message": str(e)}), 500

if __name__ == '__main__':
    app.run()
