

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash
)
import mysql.connector

app = Flask(__name__)
app.secret_key = "change-this-secret-key"


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Amma517@",
        database="student_db"
    )


@app.route("/")
def index():
    search = request.args.get("search", "").strip()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM students
        WHERE name LIKE %s OR course LIKE %s
        ORDER BY id DESC
    """, (f"%{search}%", f"%{search}%"))

    students = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "index.html",
        students=students,
        search=search
    )


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()
        course = request.form["course"].strip()

        if not name or not email or not course:
            flash("Please fill in all required fields.")
            return redirect(url_for("add_student"))

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO students (name, email, phone, course)
                VALUES (%s, %s, %s, %s)
            """, (name, email, phone, course))

            conn.commit()
            flash("Student added successfully!")

        except mysql.connector.IntegrityError:
            conn.rollback()
            flash("This email is already registered.")

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("index"))

    return render_template("add_student.html")


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()
        course = request.form["course"].strip()

        if not name or not email or not course:
            cursor.close()
            conn.close()
            flash("Please fill in all required fields.")
            return redirect(
                url_for("edit_student", student_id=student_id)
            )

        try:
            cursor.execute("""
                UPDATE students
                SET name=%s, email=%s, phone=%s, course=%s
                WHERE id=%s
            """, (name, email, phone, course, student_id))

            if cursor.rowcount == 0:
                conn.rollback()
                flash("No changes made or student not found.")
            else:
                conn.commit()
                flash("Student updated successfully!")

        except mysql.connector.IntegrityError:
            conn.rollback()
            flash("That email is already used by another student.")

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("index"))

    cursor.execute(
        "SELECT * FROM students WHERE id=%s", (student_id,)
    )
    student = cursor.fetchone()

    cursor.close()
    conn.close()

    if student is None:
        flash("Student not found.")
        return redirect(url_for("index"))

    return render_template("edit_student.html", student=student)


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=%s", (student_id,)
    )

    if cursor.rowcount:
        conn.commit()
        flash("Student deleted successfully!")
    else:
        conn.rollback()
        flash("Student not found.")

    cursor.close()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
