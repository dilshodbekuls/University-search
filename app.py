from flask import Flask, jsonify, request, make_response
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/Universities"
mongo = PyMongo(app)

# Get all universities
@app.route("/universities", methods=["GET"])
def get_universities():
    universities = list(mongo.db.universities.find())
    for uni in universities:
        uni["_id"] = str(uni["_id"])
    return jsonify(universities)

# Get a specific university by ID
@app.route("/universities/<id>", methods=["GET"])
def get_university(id):
    university = mongo.db.universities.find_one({"_id": ObjectId(id)})
    if university:
        university["_id"] = str(university["_id"])
        return jsonify(university)
    return jsonify({"msg": "University not found"}), 404

# Add a new university
@app.route("/universities", methods=["POST"])
def add_university():
    data = request.form
    if data and "displayName" in data and "city" in data and "ranking" in data:
        new_university = {
            "displayName": data.get("displayName"),
            "city": data.get("city"),
            "ranking": data.get("ranking"),
            "tuition": data.get("tuition", 0),
            "acceptance-rate": data.get("acceptance-rate", 0),
            "reviews": []
        }
        inserted_id = mongo.db.universities.insert_one(new_university).inserted_id
        new_university_link = f"http://localhost:5000/universities/{str(inserted_id)}"
        return make_response(jsonify({"URL": new_university_link}), 200)
    else:
        return make_response(jsonify({"Error": "Missing data"}), 404)

# Update a university
@app.route("/universities/<id>", methods=["PUT"])
def update_university(id):
    data = request.json if request.is_json else request.form.to_dict()
    if not data:
        return jsonify({"msg": "No update data provided"}), 400
    
    result = mongo.db.universities.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"msg": "University not found"}), 404
    return jsonify({"msg": "University updated successfully"})

# Delete a university
@app.route("/universities/<id>", methods=["DELETE"])
def delete_university(id):
    mongo.db.universities.delete_one({"_id": ObjectId(id)})
    return jsonify({"msg": "University deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True,port = 5001)
