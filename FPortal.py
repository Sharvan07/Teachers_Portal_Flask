from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initial details
user_credentials = {"Teacher 1": "111", "Teacher 2": "222"}

# Initialize data
student_names = ["Student 1", "Student 2", "Student 3", "Student 4", "Student 5", "Student 6"]


quiz_marks = {"Teacher 1": [0] * len(student_names), "Teacher 2": [0] * len(student_names)}
mid_marks = {"Teacher 1": [0] * len(student_names), "Teacher 2": [0] * len(student_names)}
terminal_marks = {"Teacher 1": [0] * len(student_names), "Teacher 2": [0] * len(student_names)}

attendance_data = {"Teacher 1": [""] * len(student_names), "Teacher 2": [""] * len(student_names)}


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in user_credentials and user_credentials[username] == password:
            return redirect(url_for('teacher_portal', username=username))
        else:
            return render_template('login.html', error=True)

    return render_template('login.html', error=False)


@app.route('/teacher_portal/<username>', methods=['GET', 'POST'])
def teacher_portal(username):
    if request.method == 'POST':
        desire_option = int(request.form['desire_option'])

        if desire_option == 1:
            # Insert marks
            return render_template('insert_marks.html', username=username, student_names=student_names)

        elif desire_option == 2:
            # Insert attendance
            return render_template('insert_attendance.html', username=username, student_names=student_names)

        elif desire_option == 3:
            # View marks
            return render_template('view_marks.html', username=username, student_names=student_names,
                                   quiz_marks=quiz_marks[username], mid_marks=mid_marks[username],
                                   terminal_marks=terminal_marks[username])

        elif desire_option == 4:
            # View attendance
            return render_template('view_attendance.html', username=username, student_names=student_names,
                                   attendance_data=attendance_data[username])

        elif desire_option == 5:
            return redirect(url_for('login'))

    return render_template('teacher_portal.html', username=username, student_names=student_names)


@app.route('/insert_marks/<username>', methods=['POST'])
@app.route('/insert_marks/<username>', methods=['GET', 'POST'])
def insert_marks(username):
    if request.method == 'POST':
        quiz_1_marks = [int(request.form[f'quiz_1_{i}']) for i in range(len(student_names))]
        quiz_2_marks = [int(request.form[f'quiz_2_{i}']) for i in range(len(student_names))]
        mid_marks = [int(request.form[f'mid_{i}']) for i in range(len(student_names))]
        terminal_marks = [int(request.form[f'terminal_{i}']) for i in range(len(student_names))]

        return redirect(url_for('success'))

    return render_template('insert_marks.html', username=username, student_names=student_names)


@app.route('/insert_attendance/<username>', methods=['POST'])
def insert_attendance(username):
    lab_attendance = [request.form[f'lab_{i}'] for i in range(len(student_names))]
    class_attendance = [request.form[f'class_{i}'] for i in range(len(student_names))]

    attendance_data[username] = lab_attendance

    return redirect(url_for('teacher_portal', username=username))


if __name__ == '__main__':
    app.run(debug=True)
