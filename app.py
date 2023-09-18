from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initial details
users = {"Teacher 1": "111", "Teacher 2": "222"}
student_names = ["Student 1", "Student 2", "Student 3", "Student 4", "Student 5", "Student 6"]

# Initialize marks and attendance data (You can use databases for a real application)
marks_data = {
    "Teacher 1": {"Quiz 1": [0] * len(student_names), "Quiz 2": [0] * len(student_names),
                   "Mid": [0] * len(student_names), "Terminal": [0] * len(student_names)},
    "Teacher 2": {"Quiz 1": [0] * len(student_names), "Quiz 2": [0] * len(student_names),
                   "Mid": [0] * len(student_names), "Terminal": [0] * len(student_names)}
}

attendance_data = {
    "Teacher 1": {"Lab": [""] * len(student_names), "Class": [""] * len(student_names)},
    "Teacher 2": {"Lab": [""] * len(student_names), "Class": [""] * len(student_names)}
}


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid username or password"
    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    if request.method == "POST":
        operation = request.form["operation"]

        if operation == "Insert Marks":
            return redirect(url_for("insert_marks"))
        elif operation == "Insert Attendance":
            return redirect(url_for("insert_attendance"))
        elif operation == "View Marks":
            return redirect(url_for("view_marks"))
        elif operation == "View Attendance":
            return redirect(url_for("view_attendance"))
        elif operation == "Logout":
            session.pop("username", None)
            return redirect(url_for("login"))

    return render_template("dashboard.html", username=username)


@app.route("/insert_marks", methods=["GET", "POST"])
def insert_marks():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    if request.method == "POST":
        assessment_type = request.form["assessment_type"]
        marks = list(map(int, request.form.getlist("marks")))

        if assessment_type not in marks_data[username]:
            return "Invalid assessment type"

        marks_data[username][assessment_type] = marks

        return redirect(url_for("dashboard"))

    return render_template("insert_marks.html", username=username, student_names=student_names)



@app.route("/insert_attendance", methods=["GET", "POST"])
def insert_attendance():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    if request.method == "POST":
        attendance_type = request.form["attendance_type"]
        attendance_status = request.form["attendance_status"]

        if attendance_type not in attendance_data[username]:
            return "Invalid attendance type"

        attendance_data[username][attendance_type] = [attendance_status] * len(student_names)

        return redirect(url_for("dashboard"))

    return render_template("insert_attendance.html", username=username, student_names=student_names)



@app.route("/view_marks", methods=["GET", "POST"])
def view_marks():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    return render_template("view_marks.html", username=username, student_names=student_names,
                           marks_data=marks_data[username])


@app.route("/view_attendance", methods=["GET", "POST"])
def view_attendance():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    return render_template("view_attendance.html", username=username, student_names=student_names,
                           attendance_data=attendance_data[username])


if __name__ == "__main__":
    app.run(debug=True)
