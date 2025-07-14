# This file will have the database models that we will use in our application.
from flask_security.core import UserMixin
from datetime import datetime

# Imports from other files
from .database import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'spoc', 'faculty'; NOTE that we won't be using the formal RBAC from flask-security. 
    created_at = db.Column(db.DateTime, default=datetime.now())

    spoc = db.relationship("SPOC", backref="user", uselist=False) # One-to-one relationship with SPOC; this relation will be use only if the user is a SPOC
    faculty = db.relationship("Faculty", backref="user", uselist=False) # One-to-one relationship with Faculty; this relation will be use only if the user is a Faculty

class College(db.Model):
    __tablename__ = 'colleges'

    id = db.Column(db.Integer, primary_key=True)
    # Basic details of the college
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(10))

    spoc = db.relationship("SPOC", backref="college", uselist=False) # One-to-one relationship with SPOC; each college has only one SPOC
    faculty = db.relationship("Faculty", backref="college", lazy=True) # One-to-many relationship with Faculty; each college can have many faculty; college.faculty will return a list of faculty objects; faculty.college will return the (single) college object
    students = db.relationship("Student", backref="college", lazy=True) # One-to-many relationship with Students; each college can have many students; college.students will return a list of student objects; student.college will return the (single) college object
    # courses = db.relationship("Course", backref="college", lazy=True) # One-to-many relationship with Courses; each college can have many courses # DOUBTFUL. CLARIFY ASAP. COMMENTED FOR NOW, SEEMS INCORRECT RELATIONSHIP

class SPOC(db.Model):
    __tablename__ = 'spocs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False) # One-to-one relationship with User; each SPOC is associated with only one user
    name = db.Column(db.String(100), nullable=False)
    personal_email = db.Column(db.String(255), nullable=False, unique=True)
    official_email = db.Column(db.String(255), nullable=False, unique=True) # This email id will be provided by IITM to the user; User will use this email id for logging in to his dashboard
    designation = db.Column(db.String(100), nullable=False) # DOUBTFUL. CLARIFY ASAP. IS THIS REALLY NEEDED?
    contact_number = db.Column(db.String(15), nullable=False, unique=True)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), unique=True, nullable=False) # One-to-one relationship with College; each SPOC is associated with only one college

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)


class StudentCourse(db.Model):
    __tablename__ = 'student_courses'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    quiz1 = db.Column(db.Float, nullable=True, default=-1) # -1 means there was no quiz for that subject. 0 means the student has not attempted the quiz; null means quiz is yet to be conducted.
    quiz2 = db.Column(db.Float, nullable=True, default=-1)
    end_term_quiz = db.Column(db.Float, nullable=True, default=-1)

    student = db.relationship("Student", backref="student_courses") # One-to-many relationship with Student; each student can have many courses
    course = db.relationship("Course", backref="student_courses")

class Faculty(db.Model):
    __tablename__ = 'faculty'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    courses = db.relationship("Course", secondary=StudentCourse, backref="students")
    course = db.relationship("Course", backref="faculty_member", uselist=False)


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), unique=True, nullable=True)