import os
import secrets
from flask import Flask, request, jsonify
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

csrf = CSRFProtect(app)

students = [
    {"id": 1, "name": "John Smith", "email": "john@gmail.com", "course": "Computer Programming"},
    {"id": 2, "name": "Sarah Brown", "email": "sarah@gmail.com", "course": "Software Engineering"},
    {"id": 3, "name": "David Wilson", "email": "david@gmail.com", "course": "Computer Programming"}
]


@app.route("/")
def home():
    return jsonify({"message": "Welcome to Student Management System"})


@app.route("/students", methods=["GET"])
def get_students():
    result = []
    unused_variable = "This variable is not used"

    for student in students:
        if student["id"] > 0:
            if student["name"] != "":
                if student["email"] != "":
                    result.append(student)

    return jsonify(result)


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    for student in students:
        if student["id"] == student_id:
            return jsonify(student)

    return jsonify({"error": "Student not found"}), 404


@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)

    required_fields = ["name", "email", "course"]

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid student data"}), 400

    for field in required_fields:
        if not isinstance(data.get(field), str) or not data[field].strip():
            return jsonify({"error": f"{field.capitalize()} is required"}), 400

    new_id = max([student["id"] for student in students], default=0) + 1

    new_student = {
        "id": new_id,
        "name": data["name"].strip(),
        "email": data["email"].strip(),
        "course": data["course"].strip()
    }

    students.append(new_student)

    return jsonify(new_student), 201


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid student data"}), 400

    allowed_fields = ["name", "email", "course"]
    updates = {}

    for field in allowed_fields:
        if field in data:
            if not isinstance(data[field], str) or not data[field].strip():
                return jsonify({"error": f"{field.capitalize()} cannot be empty"}), 400

            updates[field] = data[field].strip()

    if not updates:
        return jsonify({"error": "No valid fields provided"}), 400

    for student in students:
        if student["id"] == student_id:
            student.update(updates)
            return jsonify(student)

    return jsonify({"error": "Student not found"}), 404

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return jsonify({"message": "Student deleted successfully"})

    return jsonify({"error": "Student not found"}), 404


@app.route("/search", methods=["GET"])
def search_students():
    name = request.args.get("name", "")
    course = request.args.get("course", "")
    results = []

    for student in students:
        if name:
            if name.lower() in student["name"].lower():
                if course:
                    if course.lower() in student["course"].lower():
                        results.append(student)
                else:
                    results.append(student)
        elif course:
            if course.lower() in student["course"].lower():
                results.append(student)
        else:
            results.append(student)

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=False)
