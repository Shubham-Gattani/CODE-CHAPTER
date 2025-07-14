"""FUTURE MODIFICATIONS/# DOUBTS: # ASK, # NOTE, # TODO

2. Message from Kamala Mam: 

We need to showcase everything that the student does, in the dashboard, so that the college has visibility
Such as Regn details, fee payment, progress(ASK if it's GRAde, credits, or the level of the program), exam centre(ASK/brain_storm) , hall ticket(ASK/brain_storm), results etc. BUT HOW DO I EMBED THIS IN THE CURRENT DATABASE STRUCTURE? DO WE NEED TO ADD A NEW TABLE LIKE STUDENT_DASHBOARD?

regn_details = (email, course_code, course_name, term-year, completion_status, fee_payment_status= "un/paid")...one row for each course; INFACT, regn_details can be added directly in the enrollment_table itself

SOLUTION: { Regn details, fee_payment, hall ticket } can be added to the enrollment table itself. Even if there will be redundancy, it will keep the schema simple. Later on we can do normalization if required. Main thing to keep in mind here is that regn_details is different for course-enrollment; while fee_payment and hall_ticket are dependent on [student_id, year_term] 
For results, we already have a table named quiz. 

3. SUGGESTION FROM GPT: You mention wanting to show all student activities.
Suggestion: Instead of a new table, consider adding relationships or views that aggregate data from existing tables (registrations, payments, progress, results, etc.).
If you need to store dashboard-specific data, create a StudentActivityLog table.
4. SUGGESTION FROM GPT: Consider adding indexes on frequently queried fields (e.g., email, college_id).

# ASK: I guess we do have to store information of students submitting graded/practice/bonus assignments? In that case, we can create a seperate table named "assignment_scores" which will have 1-1 relation with enrollment table.
"""
# This file will have the database models that we will use in our application.
from flask_security.core import UserMixin, RoleMixin
from datetime import datetime
import uuid

# Imports from other files
from .database import db

class Role(db.Model, RoleMixin):
    """
    Represents user roles in the system (admin, spoc, faculty). 
    This model is defined first to avoid circular dependency issues.
    """
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(100))

    # RELATIONSHIPS (defined after roles_users table)
    users = db.relationship('User', secondary='roles_users', back_populates='roles')

# Define the association table AFTER the Role model
roles_users = db.Table( # Added only to avoid errors related to flask-security. We won't be using the formal RBAC from flask-security.
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)
class User(db.Model, UserMixin):
    """
    Represents a system user, which can be an admin, SPOC, or faculty member. Stores authentication and role information.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False) # For SPOC and Faculty, this will be the official email id provided by IITM
    password = db.Column(db.String(255), nullable=False)
    
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'spoc', 'faculty'; NOTE that we won't be using the formal RBAC from flask-security. 
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # RELATIONSHIPS
    spoc = db.relationship("SPOC", back_populates="user", uselist=False) # One-to-one relationship with SPOC; this relation will be use only if the user is a SPOC
    faculty = db.relationship("Faculty", back_populates="user", uselist=False) # One-to-one relationship with Faculty; this relation will be use only if the user is a Faculty
    roles = db.relationship('Role', secondary=roles_users,
                            back_populates='users') # Added to avoid errors related to flask-security.

class College(db.Model):
    """
    Represents a college participating in the program, including its basic details and relationships to SPOC, faculty, and students.
    """
    __tablename__ = 'colleges'

    id = db.Column(db.Integer, primary_key=True)
    # Basic details of the college
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(10))

    # RELATIONSHIPS

    spoc = db.relationship("SPOC", back_populates="college", uselist=False) # One-to-one relationship with SPOC; each college has only one SPOC
    faculty = db.relationship("Faculty", back_populates="college", lazy=True) # One-to-many relationship with Faculty; each college can have many faculty; college.faculty will return a list of faculty objects; faculty.college will return the (single) college object
    students = db.relationship('Student', back_populates='college', lazy=True) # One-to-many relationship with Students; each college can have many students; college.students will return a list of student objects; student.college will return the (single) college object
    student_courses = db.relationship('StudentCourse', back_populates='college', lazy=True)

class SPOC(db.Model):
    """
    Represents the Single Point of Contact for a college, linking a user account to a specific college and storing SPOC-specific details.
    """
    __tablename__ = 'spocs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False) # One-to-one relationship with User; each SPOC is associated with only one user
    name = db.Column(db.String(100), nullable=False)
    personal_email = db.Column(db.String(255), nullable=False, unique=True)
    designation = db.Column(db.String(100), nullable=False) # e.g HOD, Director, etc.
    contact_number = db.Column(db.String(15), nullable=False, unique=True)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), unique=True, nullable=False) # One-to-one relationship with College; each SPOC is associated with only one college

    # RELATIONSHIPS
    user = db.relationship("User", back_populates="spoc", uselist=False)
    college = db.relationship("College", back_populates="spoc", uselist=False)

class Faculty(db.Model):
    """
    Represents a faculty member associated with a college, linking a user account to faculty-specific details and the courses they teach.
    """
    __tablename__ = 'faculty'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)  # One-to-one with User
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)         # Each faculty must belong to one college
    name = db.Column(db.String(100), nullable=False)
    personal_email = db.Column(db.String(255), nullable=False, unique=True) #   Sqlite does not allow a field to be nullable and Unique at the same time.
    contact_number = db.Column(db.String(15), nullable=False, unique=True)

    # RELATIONSHIPS

    # One-to-many with CollegeCourse (each faculty can teach zero or more collegeCourse, and each collegeCourse can have zero or more faculty)
    user = db.relationship("User", back_populates="faculty", uselist=False)
    college = db.relationship("College", back_populates="faculty")

class Student(db.Model):
    """
    Represents a student enrolled in a college, storing personal and contact information, and linking to their quiz records.
    """
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    personal_email = db.Column(db.String(255), unique=True, nullable=False)  # FIXED: Made non-nullable since it's used as FK target
    contact_number = db.Column(db.String(15), unique=True, nullable=True)

    # RELATIONSHIPS
    college = db.relationship('College', back_populates='students')
    
    courses = db.relationship(
        'StudentCourse',
        back_populates='student',
        lazy=True
    )
    
class StudentCourse(db.Model):
    """
    Represents a student's registration for a course in a particular term.
    """
    __tablename__ = 'student_courses'
    
    # Add an ID as primary key for better design
    id = db.Column(db.Integer, primary_key=True)
    
    college_id = db.Column(db.Integer, db.ForeignKey("colleges.id"), nullable=False)
    personal_email = db.Column(db.String(255), db.ForeignKey('students.personal_email'), nullable=False)  # FK
    student_email = db.Column(db.String(255), nullable=False)
    account_id = db.Column(db.Integer)
    course_registration_type = db.Column(db.String, nullable=False)
    course_name = db.Column(db.String, nullable=True)
    course_code = db.Column(db.String, nullable=False)
    term_code = db.Column(db.String, nullable=False)
    application_status = db.Column(db.String, nullable=True)
    application_id = db.Column(db.Integer, nullable=True)

    # Add unique constraint for the business logic
    __table_args__ = (
        db.UniqueConstraint('student_email', 'course_registration_type', 'course_code', 'term_code', 
                           name='uq_student_course_enrollment'),
    )

    # Relationships - SQLAlchemy will automatically use the FK
    student = db.relationship( 
        'Student',
        back_populates='courses'
    )

    college = db.relationship('College', back_populates='student_courses')

    marks = db.relationship(
        'StudentMarks',
        back_populates='student_course',
        lazy=True
    )

class StudentMarks(db.Model):
    """
    Represents a student's marks for a specific test/assessment/GradedAssignment in a course and term.
    """
    __tablename__ = 'student_marks'

    id = db.Column(db.Integer, primary_key=True)  # FIXED: Added proper primary key
    student_course_id = db.Column(db.Integer, db.ForeignKey('student_courses.id'), nullable=False)  # FIXED: Proper FK to StudentCourse
    
    email = db.Column(db.String, nullable=True)
    student_email = db.Column(db.String, nullable=False)  # Keep for data consistency but not as FK
    account_id = db.Column(db.Integer, nullable=True)
    course_code = db.Column(db.String, nullable=False)
    course_name = db.Column(db.String, nullable=True)
    current_level = db.Column(db.String, nullable=True)
    marks_level = db.Column(db.String, nullable=False)
    marks = db.Column(db.Float, nullable=True)
    grade = db.Column(db.String, nullable=True)
    result = db.Column(db.String, nullable=True)
    test_code = db.Column(db.String, nullable=False) # ASSIGNMENT-11, WEEK05_GRPA06, COURSE_SCORE etc.
    term_code = db.Column(db.String, nullable=False)
    order = db.Column(db.Integer, nullable=True) # Represents the term number from starting of the degree

    # Add unique constraint for the business logic
    __table_args__ = (
    db.UniqueConstraint('student_email', 'course_code', 'term_code', 'test_code', 'marks_level', 
                       name='uq_student_marks'),
)

    # Simplified relationship using the new FK
    student_course = db.relationship(
        'StudentCourse',
        back_populates='marks'
    )