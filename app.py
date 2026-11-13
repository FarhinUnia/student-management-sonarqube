
from flask import Flask, request, jsonify

app = Flask(__name__)

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
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid student data"}), 400

    if "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    if "email" not in data:
        return jsonify({"error": "Email is required"}), 400

    if "course" not in data:
        return jsonify({"error": "Course is required"}), 400

    new_id = max([student["id"] for student in students], default=0) + 1

    new_student = {
        "id": new_id,
        "name": data["name"],
        "email": data["email"],
        "course": data["course"]
    }

    students.append(new_student)

    return jsonify(new_student), 201


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json()

    try:
        for student in students:
            if student["id"] == student_id:
                if "name" in data:
                    student["name"] = data["name"]
                if "email" in data:
                    student["email"] = data["email"]
                if "course" in data:
                    student["course"] = data["course"]

                return jsonify(student)

        return jsonify({"error": "Student not found"}), 404

    except Exception:
        return jsonify({"error": "Something went wrong"}), 500


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
    app.run(debug=True)
