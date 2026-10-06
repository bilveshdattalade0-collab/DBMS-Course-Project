from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1710",
        database="examination_db"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/")
def index():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM STUDENT")
    students = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM COURSE")
    courses = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM EXAMINATION")
    examinations = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM EXAM_HALL")
    halls = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT
            e.Exam_ID,
            c.Course_Name,
            e.Exam_Date
        FROM EXAMINATION e
        JOIN COURSE c
            ON e.Course_ID = c.Course_ID
        ORDER BY e.Exam_Date
    """)

    exams = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        page="dashboard",
        students=students,
        courses=courses,
        examinations=examinations,
        halls=halls,
        exams=exams
    )


# =========================================================
# STUDENTS
# =========================================================

@app.route("/students")
def students_page():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            Student_ID,
            Name,
            Branch,
            Semester
        FROM STUDENT
        ORDER BY Student_ID
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        page="students",
        data=data
    )


# =========================================================
# ADD STUDENT
# =========================================================

@app.route("/students/add", methods=["POST"])
def add_student():

    student_id = request.form["student_id"]
    name = request.form["name"]
    branch = request.form["branch"]
    semester = request.form["semester"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO STUDENT
        (Student_ID, Name, Branch, Semester)
        VALUES (%s, %s, %s, %s)
    """, (student_id, name, branch, semester))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/students")


# =========================================================
# EDIT STUDENT
# =========================================================

@app.route("/students/edit/<int:student_id>")
def edit_student(student_id):

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            Student_ID,
            Name,
            Branch,
            Semester
        FROM STUDENT
        WHERE Student_ID = %s
    """, (student_id,))

    student = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        page="edit_student",
        student=student
    )


# =========================================================
# UPDATE STUDENT
# =========================================================

@app.route("/students/update/<int:student_id>", methods=["POST"])
def update_student(student_id):

    name = request.form["name"]
    branch = request.form["branch"]
    semester = request.form["semester"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE STUDENT
        SET
            Name = %s,
            Branch = %s,
            Semester = %s
        WHERE Student_ID = %s
    """, (name, branch, semester, student_id))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/students")


# =========================================================
# DELETE STUDENT
# =========================================================

@app.route("/students/delete/<int:student_id>")
def delete_student(student_id):

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM STUDENT
        WHERE Student_ID = %s
    """, (student_id,))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/students")


# =========================================================
# COURSES
# =========================================================

@app.route("/courses")
def courses_page():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            Course_ID,
            Course_Name,
            Credits
        FROM COURSE
        ORDER BY Course_ID
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        page="courses",
        data=data
    )
@app.route("/courses/add", methods=["POST"])
def add_course():
    course_id = request.form["course_id"]
    course_name = request.form["course_name"]
    credits = request.form["credits"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO COURSE (Course_ID, Course_Name, Credits)
        VALUES (%s, %s, %s)
    """, (course_id, course_name, credits))

    db.commit()
    cursor.close()
    db.close()

    return redirect("/courses")
@app.route("/courses/delete/<int:course_id>")
def delete_course(course_id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM COURSE
        WHERE Course_ID = %s
    """, (course_id,))

    db.commit()
    cursor.close()
    db.close()

    return redirect("/courses")


# =========================================================
# EXAMINATIONS
# =========================================================

@app.route("/examinations")
def examinations_page():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            e.Exam_ID,
            e.Course_ID,
            c.Course_Name,
            e.Exam_Date
        FROM EXAMINATION e
        JOIN COURSE c
            ON e.Course_ID = c.Course_ID
        ORDER BY e.Exam_Date
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        page="examinations",
        data=data
    )


# =========================================================
# ADD EXAMINATION
# =========================================================

@app.route("/examinations/add", methods=["POST"])
def add_examination():

    exam_id = request.form["exam_id"]
    course_id = request.form["course_id"]
    exam_date = request.form["exam_date"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO EXAMINATION
        (Exam_ID, Course_ID, Exam_Date)
        VALUES (%s, %s, %s)
    """, (exam_id, course_id, exam_date))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/examinations")


# =========================================================
# EDIT EXAMINATION
# =========================================================

@app.route("/examinations/edit/<int:exam_id>")
def edit_examination(exam_id):

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            Exam_ID,
            Course_ID,
            Exam_Date
        FROM EXAMINATION
        WHERE Exam_ID = %s
    """, (exam_id,))

    exam = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        page="edit_examination",
        exam=exam
    )


# =========================================================
# UPDATE EXAMINATION
# =========================================================

@app.route("/examinations/update/<int:exam_id>", methods=["POST"])
def update_examination(exam_id):

    course_id = request.form["course_id"]
    exam_date = request.form["exam_date"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE EXAMINATION
        SET
            Course_ID = %s,
            Exam_Date = %s
        WHERE Exam_ID = %s
    """, (course_id, exam_date, exam_id))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/examinations")


# =========================================================
# DELETE EXAMINATION
# =========================================================

@app.route("/examinations/delete/<int:exam_id>")
def delete_examination(exam_id):

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM EXAMINATION
        WHERE Exam_ID = %s
    """, (exam_id,))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/examinations")


# =========================================================
# FACULTY
# =========================================================

@app.route("/faculty")
def faculty_page():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            Faculty_ID,
            Faculty_Name
        FROM FACULTY
        ORDER BY Faculty_ID
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        page="faculty",
        data=data
    )


# =========================================================
# ADD FACULTY
# =========================================================

@app.route("/faculty/add", methods=["POST"])
def add_faculty():

    faculty_id = request.form["faculty_id"]
    faculty_name = request.form["faculty_name"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO FACULTY
        (Faculty_ID, Faculty_Name)
        VALUES (%s, %s)
    """, (faculty_id, faculty_name))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/faculty")


# =========================================================
# DELETE FACULTY
# =========================================================

@app.route("/faculty/delete/<int:faculty_id>")
def delete_faculty(faculty_id):

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM FACULTY
        WHERE Faculty_ID = %s
    """, (faculty_id,))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/faculty")


# =========================================================
# EXAM HALLS
# =========================================================

@app.route("/halls")
def halls_page():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            Hall_ID,
            Hall_Name,
            Capacity
        FROM EXAM_HALL
        ORDER BY Hall_ID
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        page="halls",
        data=data
    )


# =========================================================
# ADD EXAM HALL
# =========================================================

@app.route("/halls/add", methods=["POST"])
def add_hall():

    hall_id = request.form["hall_id"]
    hall_name = request.form["hall_name"]
    capacity = request.form["capacity"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO EXAM_HALL
        (Hall_ID, Hall_Name, Capacity)
        VALUES (%s, %s, %s)
    """, (hall_id, hall_name, capacity))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/halls")


# =========================================================
# EDIT EXAM HALL
# =========================================================

@app.route("/halls/edit/<int:hall_id>")
def edit_hall(hall_id):

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            Hall_ID,
            Hall_Name,
            Capacity
        FROM EXAM_HALL
        WHERE Hall_ID = %s
    """, (hall_id,))

    hall = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        page="edit_hall",
        hall=hall
    )


# =========================================================
# UPDATE EXAM HALL
# =========================================================

@app.route("/halls/update/<int:hall_id>", methods=["POST"])
def update_hall(hall_id):

    hall_name = request.form["hall_name"]
    capacity = request.form["capacity"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE EXAM_HALL
        SET
            Hall_Name = %s,
            Capacity = %s
        WHERE Hall_ID = %s
    """, (hall_name, capacity, hall_id))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/halls")


# =========================================================
# DELETE EXAM HALL
# =========================================================

@app.route("/halls/delete/<int:hall_id>")
def delete_hall(hall_id):

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM EXAM_HALL
        WHERE Hall_ID = %s
    """, (hall_id,))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/halls")


# =========================================================
# HALL ALLOCATION
# =========================================================

@app.route("/hall-allocation")
def hall_allocation_page():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            h.Exam_ID,
            h.Hall_ID,
            eh.Hall_Name
        FROM HALL_ALLOCATION h
        JOIN EXAM_HALL eh
            ON h.Hall_ID = eh.Hall_ID
        ORDER BY h.Exam_ID
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        page="hall_allocation",
        data=data
    )


# =========================================================
# ADD HALL ALLOCATION
# =========================================================

@app.route("/hall-allocation/add", methods=["POST"])
def add_hall_allocation():

    exam_id = request.form["exam_id"]
    hall_id = request.form["hall_id"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO HALL_ALLOCATION
        (Exam_ID, Hall_ID)
        VALUES (%s, %s)
    """, (exam_id, hall_id))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/hall-allocation")
# =========================================================
# DELETE HALL ALLOCATION
# =========================================================

@app.route("/hall-allocation/delete/<int:exam_id>/<int:hall_id>")
def delete_hall_allocation(exam_id, hall_id):

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM HALL_ALLOCATION
        WHERE Exam_ID = %s
        AND Hall_ID = %s
    """, (exam_id, hall_id))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/hall-allocation")

# =========================================================
# INVIGILATORS
# =========================================================

@app.route("/invigilators")
def invigilators_page():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            ei.Exam_ID,
            ei.Faculty_ID,
            f.Faculty_Name
        FROM EXAM_INVIGILATOR ei
        JOIN FACULTY f
            ON ei.Faculty_ID = f.Faculty_ID
        ORDER BY ei.Exam_ID
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        page="invigilators",
        data=data
    )


# =========================================================
# ADD INVIGILATOR
# =========================================================

@app.route("/invigilators/add", methods=["POST"])
def add_invigilator():

    exam_id = request.form["exam_id"]
    faculty_id = request.form["faculty_id"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO EXAM_INVIGILATOR
        (Exam_ID, Faculty_ID)
        VALUES (%s, %s)
    """, (exam_id, faculty_id))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/invigilators")


# =========================================================
# MARKS
# =========================================================

@app.route("/marks")
def marks_page():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            m.Marks_ID,
            m.Student_ID,
            s.Name,
            m.Exam_ID,
            m.Marks_Obtained
        FROM MARKS m
        JOIN STUDENT s
            ON m.Student_ID = s.Student_ID
        ORDER BY m.Marks_ID
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        page="marks",
        data=data
    )


# =========================================================
# ADD MARKS
# =========================================================

@app.route("/marks/add", methods=["POST"])
def add_marks():

    marks_id = request.form["marks_id"]
    student_id = request.form["student_id"]
    exam_id = request.form["exam_id"]
    marks_obtained = request.form["marks_obtained"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO MARKS
        (Marks_ID, Student_ID, Exam_ID, Marks_Obtained)
        VALUES (%s, %s, %s, %s)
    """, (
        marks_id,
        student_id,
        exam_id,
        marks_obtained
    ))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/marks")

# =========================================================
# DELETE MARKS
# =========================================================

@app.route("/marks/delete/<int:marks_id>")
def delete_marks(marks_id):

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM MARKS
        WHERE Marks_ID = %s
    """, (marks_id,))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/marks")
# =========================================================
# RESULTS
# =========================================================

@app.route("/results")
def results_page():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.Result_ID,
            r.Student_ID,
            s.Name,
            r.Course_ID,
            c.Course_Name,
            r.Grade,
            r.Status
        FROM RESULT r
        JOIN STUDENT s
            ON r.Student_ID = s.Student_ID
        JOIN COURSE c
            ON r.Course_ID = c.Course_ID
        ORDER BY r.Result_ID
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        page="results",
        data=data
    )


# =========================================================
# ADD RESULT
# =========================================================

@app.route("/results/add", methods=["POST"])
def add_result():

    result_id = request.form["result_id"]
    student_id = request.form["student_id"]
    course_id = request.form["course_id"]
    grade = request.form["grade"]
    status = request.form["status"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO RESULT
        (Result_ID, Student_ID, Course_ID, Grade, Status)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        result_id,
        student_id,
        course_id,
        grade,
        status
    ))

    db.commit()

    cursor.close()
    db.close()

    return redirect("/results")

@app.route("/results/delete/<int:result_id>")
def delete_result(result_id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM RESULT
        WHERE Result_ID = %s
    """, (result_id,))

    db.commit()
    cursor.close()
    db.close()

    return redirect("/results")
# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)