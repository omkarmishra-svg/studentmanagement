from flask import Flask, request, jsonify, send_from_directory, abort, g
from flask_cors import CORS
from db import init_db, get_db
from models import calculate_percentage_and_grade
import os
import traceback
import sqlite3

app = Flask(__name__, static_folder="frontend", static_url_path="/")
CORS(app)  # not strictly necessary if serving static from same server

# Initialize DB
try:
    init_db()
except Exception as e:
    print(f"Database initialization error: {e}")
    traceback.print_exc()


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# ---------- API routes ----------
@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    try:
        roll = int(data["roll"])
        name = data.get("name", "")[:50]
        age = int(data.get("age", 0))
        branch = data.get("branch", "")[:30]
        marks = [
            float(data.get(f"mark{i+1}", 0.0)) for i in range(5)
        ]
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid data"}), 400

    student = {
        "roll": roll,
        "name": name,
        "age": age,
        "branch": branch,
        "mark1": marks[0],
        "mark2": marks[1],
        "mark3": marks[2],
        "mark4": marks[3],
        "mark5": marks[4],
        "percentage": 0.0,
        "grade": "F"
    }
    # calculate percentage & grade
    calculate_percentage_and_grade(student)

    try:
        db = get_db()
        db.execute("""
            INSERT INTO students (roll, name, age, branch, mark1, mark2, mark3, mark4, mark5, percentage, grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (student["roll"], student["name"], student["age"], student["branch"],
              student["mark1"], student["mark2"], student["mark3"], student["mark4"], student["mark5"],
              student["percentage"], student["grade"]))
        db.commit()
        return jsonify({"message": "Student added", "student": student}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Student with this roll number already exists"}), 400
    except Exception as e:
        print(f"Error in add_student: {e}")
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/api/students", methods=["GET"])
def get_students():
    try:
        db = get_db()
        cur = db.execute("SELECT * FROM students")
        rows = [dict(ix) for ix in cur.fetchall()]
        return jsonify(rows)
    except Exception as e:
        print(f"Error in get_students: {e}")
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/api/students/<int:roll>", methods=["GET"])
def get_student(roll):
    try:
        db = get_db()
        cur = db.execute("SELECT * FROM students WHERE roll = ?", (roll,))
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(dict(row))
    except Exception as e:
        print(f"Error in get_student: {e}")
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/api/students/<int:roll>", methods=["PUT"])
def update_student(roll):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON body required"}), 400

        db = get_db()
        cur = db.execute("SELECT * FROM students WHERE roll = ?", (roll,))
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Student not found"}), 404

        # existing values
        student = dict(row)
        # update fields if provided (keep existing otherwise)
        student["name"] = data.get("name", student["name"])[:50]
        student["age"] = int(data.get("age", student["age"]))
        student["branch"] = data.get("branch", student["branch"])[:30]
        for i in range(1, 6):
            key = f"mark{i}"
            if key in data:
                student[key] = float(data[key])

        # recalc
        calculate_percentage_and_grade(student)

        db.execute("""
            UPDATE students SET name=?, age=?, branch=?, mark1=?, mark2=?, mark3=?, mark4=?, mark5=?, percentage=?, grade=?
            WHERE roll=?
        """, (student["name"], student["age"], student["branch"],
              student["mark1"], student["mark2"], student["mark3"], student["mark4"], student["mark5"],
              student["percentage"], student["grade"], roll))
        db.commit()
        return jsonify({"message": "Updated", "student": student})
    except Exception as e:
        print(f"Error in update_student: {e}")
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/api/students/<int:roll>", methods=["DELETE"])
def delete_student(roll):
    try:
        db = get_db()
        cur = db.execute("DELETE FROM students WHERE roll = ?", (roll,))
        db.commit()
        if cur.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404
        return jsonify({"message": f"Student {roll} deleted"})
    except Exception as e:
        print(f"Error in delete_student: {e}")
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/api/students/sorted", methods=["GET"])
def sorted_students():
    try:
        db = get_db()
        cur = db.execute("SELECT * FROM students ORDER BY percentage DESC")
        rows = [dict(ix) for ix in cur.fetchall()]
        return jsonify(rows)
    except Exception as e:
        print(f"Error in sorted_students: {e}")
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/api/students/count", methods=["GET"])
def count_students():
    try:
        db = get_db()
        cur = db.execute("SELECT COUNT(*) as cnt FROM students")
        row = cur.fetchone()
        return jsonify({"count": row["cnt"]})
    except Exception as e:
        print(f"Error in count_students: {e}")
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# ---------- Dummy Data Endpoint ----------
@app.route("/api/students/dummy", methods=["POST"])
def add_dummy_data():
    """Add sample dummy data for testing"""
    try:
        db = get_db()
        
        # Check if data already exists
        cur = db.execute("SELECT COUNT(*) as cnt FROM students")
        count = cur.fetchone()["cnt"]
        if count > 0:
            return jsonify({"message": "Database already has data. Clear it first if you want to add dummy data.", "count": count}), 200
        
        dummy_students = [
            {"roll": 101, "name": "Rajesh Kumar", "age": 20, "branch": "Computer Science", "mark1": 95, "mark2": 92, "mark3": 88, "mark4": 90, "mark5": 94},
            {"roll": 102, "name": "Priya Sharma", "age": 21, "branch": "Electronics", "mark1": 85, "mark2": 87, "mark3": 82, "mark4": 86, "mark5": 84},
            {"roll": 103, "name": "Amit Singh", "age": 19, "branch": "Mechanical", "mark1": 75, "mark2": 78, "mark3": 72, "mark4": 76, "mark5": 74},
            {"roll": 104, "name": "Sneha Patel", "age": 20, "branch": "Computer Science", "mark1": 65, "mark2": 68, "mark3": 62, "mark4": 66, "mark5": 64},
            {"roll": 105, "name": "Vikram Reddy", "age": 22, "branch": "Civil", "mark1": 55, "mark2": 58, "mark3": 52, "mark4": 56, "mark5": 54},
            {"roll": 106, "name": "Anjali Desai", "age": 20, "branch": "Computer Science", "mark1": 98, "mark2": 96, "mark3": 99, "mark4": 97, "mark5": 98},
            {"roll": 107, "name": "Rahul Verma", "age": 21, "branch": "Electronics", "mark1": 88, "mark2": 85, "mark3": 90, "mark4": 87, "mark5": 89},
            {"roll": 108, "name": "Kavya Nair", "age": 19, "branch": "Mechanical", "mark1": 78, "mark2": 80, "mark3": 75, "mark4": 79, "mark5": 77},
            {"roll": 109, "name": "Arjun Menon", "age": 20, "branch": "Computer Science", "mark1": 92, "mark2": 94, "mark3": 91, "mark4": 93, "mark5": 95},
            {"roll": 110, "name": "Meera Iyer", "age": 21, "branch": "Electronics", "mark1": 82, "mark2": 84, "mark3": 80, "mark4": 83, "mark5": 81},
        ]
        
        added_count = 0
        for student_data in dummy_students:
            student = {
                "roll": student_data["roll"],
                "name": student_data["name"],
                "age": student_data["age"],
                "branch": student_data["branch"],
                "mark1": student_data["mark1"],
                "mark2": student_data["mark2"],
                "mark3": student_data["mark3"],
                "mark4": student_data["mark4"],
                "mark5": student_data["mark5"],
                "percentage": 0.0,
                "grade": "F"
            }
            calculate_percentage_and_grade(student)
            
            try:
                db.execute("""
                    INSERT INTO students (roll, name, age, branch, mark1, mark2, mark3, mark4, mark5, percentage, grade)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (student["roll"], student["name"], student["age"], student["branch"],
                      student["mark1"], student["mark2"], student["mark3"], student["mark4"], student["mark5"],
                      student["percentage"], student["grade"]))
                added_count += 1
            except sqlite3.IntegrityError:
                # Skip if roll already exists
                continue
        
        db.commit()
        return jsonify({"message": f"Successfully added {added_count} dummy students", "count": added_count}), 201
        
    except Exception as e:
        print(f"Error in add_dummy_data: {e}")
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# ---------- static frontend routes ----------
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_file(path):
    # serve any frontend file (add.html, edit.html, assets/...)
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        abort(404)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)