"""FUTURE MODIFICATIONS/# DOUBTS: # ASK, # NOTE, # TODO

2. Message from Kamala Mam: 

We need to showcase everything that the student does, in the dashboard, so that the college has visibility
Such as Regn details, fee payment, progress(ASK if it's GRAde, credits, or the level of the program), exam centre , hall ticket, results etc. BUT HOW DO I EMBED THIS IN THE CURRENT DATABASE STRUCTURE? DO WE NEED TO ADD A NEW TABLE LIKE STUDENT_DASHBOARD?

3. SUGGESTION FROM GPT: You mention wanting to show all student activities.
Suggestion: Instead of a new table, consider adding relationships or views that aggregate data from existing tables (registrations, payments, progress, results, etc.).
If you need to store dashboard-specific data, create a StudentActivityLog table.
4. SUGGESTION FROM GPT: Consider adding indexes on frequently queried fields (e.g., email, college_id).
"""
# This file will have the database models that we will use in our application.
from flask_security.core import UserMixin, RoleMixin
from datetime import datetime, timedelta
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
    spoc = db.relationship("SpocDetails", back_populates="user", uselist=False) # One-to-one relationship with SPOC; this relation will be use only if the user is a SPOC
    faculty = db.relationship("Faculty", back_populates="user", uselist=False) # One-to-one relationship with Faculty; this relation will be use only if the user is a Faculty
    roles = db.relationship('Role', secondary=roles_users,
                            back_populates='users') # Added to avoid errors related to flask-security.

class CollegeDetails(db.Model):
    __tablename__ = 'college_details'
    
    id = db.Column(db.Integer, primary_key=True)
    cc_id = db.Column(db.String(20), unique=True) # IMP
    college_name = db.Column(db.String(255))
    logo_path = db.Column(db.String(14))
    addr1 = db.Column(db.Text)  # mediumtext is generally mapped as Text
    aicte_approved = db.Column(db.String(20))
    city = db.Column(db.String(255))
    pincode = db.Column(db.String(10))
    college_link = db.Column(db.String(200))
    university = db.Column(db.String(255))
    mobile_no1 = db.Column(db.String(100))
    mobile_no2 = db.Column(db.String(100))
    partnering_since = db.Column(db.String(10))
    updated_at = db.Column(db.String(100))
    is_active = db.Column(db.String(10))
    stateName = db.Column(db.String(100))
    country = db.Column(db.String(255))
    instituteType = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    updated_by = db.Column(db.String(255))
    changes = db.Column(db.Text)
    mou_cloud_link = db.Column(db.String(500))
    mou_grive_link = db.Column(db.String(500))

    # RELATIONSHIPS

    spoc = db.relationship("SpocDetails", back_populates="college", uselist=False) # One-to-one relationship with SPOC; each college has only one SPOC
    faculty = db.relationship("Faculty", back_populates="college", lazy=True) # One-to-many relationship with Faculty; each college can have many faculty; college.faculty will return a list of faculty objects; faculty.college will return the (single) college object
    students = db.relationship('Student', back_populates='college', lazy=True) # One-to-many relationship with Students; each college can have many students; college.students will return a list of student objects; student.college will return the (single) college object
    student_courses = db.relationship('StudentCourse', back_populates='college', lazy=True)

class SpocDetails(db.Model):
    """
    Represents the Single Point of Contact for a college, linking a user account to a specific college and storing SPOC-specific details.
    """
    __tablename__ = 'spoc_details'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    spocName = db.Column(db.String(150))
    spoc_emailid = db.Column(db.String(150), nullable=False, unique=True)
    principal_name = db.Column(db.String(250))
    principal_email = db.Column(db.String(250))
    principal_mobile = db.Column(db.String(50))
    designation = db.Column(db.String(150)) # HOD, Professor etc
    department = db.Column(db.String(100))
    mobileNumber = db.Column(db.String(50))
    mobileNumber2 = db.Column(db.String(20))
    profile_photo = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    cc_id = db.Column(db.Integer, db.ForeignKey('college_details.id'), nullable=False)
    status = db.Column(db.String(250), nullable=False, default='Y')
    spoc_onboard = db.Column(db.Integer, nullable=False)

    # RELATIONSHIPS:
    user = db.relationship("User", back_populates="spoc", uselist=False)
    college = db.relationship("CollegeDetails", back_populates="spoc")

class Faculty(db.Model):
    """
    Represents a faculty member associated with a college, linking a user account to faculty-specific details and the courses they teach.
    """
    __tablename__ = 'faculties'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)  # One-to-one with User
    college_id = db.Column(db.Integer, db.ForeignKey('college_details.id'), nullable=False)         # Each faculty must belong to one college
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    name = db.Column(db.String(100), nullable=False)
    personal_email = db.Column(db.String(255), nullable=False, unique=True) #   Sqlite does not allow a field to be nullable and Unique at the same time.
    contact_number = db.Column(db.String(15), nullable=False, unique=True)
    profile_photo = db.Column(db.String(100), nullable=True)  # Path to the profile photo
    signature = db.Column(db.String(100), nullable=True)  # Path to the signature image
    dob = db.Column(db.String(50), nullable=True)  # Date of Birth

    # RELATIONSHIPS
    user = db.relationship("User", back_populates="faculty", uselist=False)
    college = db.relationship("CollegeDetails", back_populates="faculty")
    mentors = db.relationship("Mentor", back_populates="faculty", cascade="all, delete-orphan")
    student = db.relationship("Student", back_populates="faculty", uselist=False)  # Each faculty is a student first, and then becomes a mentor if s/he scores >8 grade in the courses for which he gave exams.


class Mentor(db.Model):
    """
    Represents a mentor, linking a faculty member to the courses they are eligible to teach.
    """
    __tablename__ = 'mentors'

    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    mentoring_term = db.Column(db.String(50), nullable=True) # This is the term code for which the faculty will be a mentor.
    course = db.Column(db.Text, nullable=True) # we need it as csv; we have to write a logic at the backend which finds the courses for which faculty has got grades>8; right now we will just insert some dummy courses as csv for demo purpose.

    # Relationships
    faculty = db.relationship("Faculty", back_populates="mentors")  # Many-to-one relationship with Faculty; each mentor is a faculty member


class Student(db.Model):
    """
    Represents a student enrolled in a college, storing personal and contact information, and linking to their quiz records.
    """
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('college_details.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    personal_email = db.Column(db.String(255), unique=True, nullable=False)  # FIXED: Made non-nullable since it's used as FK target
    contact_number = db.Column(db.String(15), unique=True, nullable=True) # HIDE IN UI
    dob = db.Column(db.String(50), nullable=True)  # Date of Birth
    profile_photo = db.Column(db.String(100), nullable=True)  # Path to the profile photo
    signature = db.Column(db.String(100), nullable=True)  # Path to the signature image
    id_card = db.Column(db.String(100), nullable=True)  # Path to the ID card image, for confirming the full name with id card
    # user_type; ask Mallika mam
    # RELATIONSHIPS
    college = db.relationship('CollegeDetails', back_populates='students')
    faculty = db.relationship("Faculty", back_populates="student", uselist=False)  # Note that a very few of these rows will be connected to a faculty.
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
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey("college_details.id"), nullable=False)
    personal_email = db.Column(db.String(255), nullable=False)  # FK
    student_email = db.Column(db.String(255), nullable=False)
    account_id = db.Column(db.Integer)
    course_registration_type = db.Column(db.String(255), nullable=False)
    course_name = db.Column(db.String(255), nullable=True)
    course_code = db.Column(db.String(255), nullable=False)
    term_code = db.Column(db.String(255), nullable=False)
    application_status = db.Column(db.String(255), nullable=True)
    application_id = db.Column(db.Integer, nullable=True)

    # Relationships - SQLAlchemy will automatically use the FK
    student = db.relationship( 
        'Student',
        back_populates='courses'
    )

    college = db.relationship('CollegeDetails', back_populates='student_courses')

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
    
    email = db.Column(db.String(255), nullable=True) # is the official email id
    student_email = db.Column(db.String(255), nullable=True)  # Keep for data consistency but not as FK
    account_id = db.Column(db.Integer, nullable=True)
    course_code = db.Column(db.String(255), nullable=False)
    course_name = db.Column(db.String(255), nullable=True)
    current_level = db.Column(db.String(255), nullable=True)
    marks_level = db.Column(db.String(255), nullable=False)
    marks = db.Column(db.Float, nullable=True)
    grade = db.Column(db.String(255), nullable=True)
    result = db.Column(db.String(255), nullable=True)
    test_code = db.Column(db.String(255), nullable=False) # ASSIGNMENT-11, WEEK05_GRPA06, COURSE_SCORE etc.
    term_code = db.Column(db.String(255), nullable=False)
    order = db.Column(db.Integer, nullable=True) # Represents the term number from starting of the degree

    # Simplified relationship using the new FK
    student_course = db.relationship(
        'StudentCourse',
        back_populates='marks'
    )

class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    expires_at = db.Column(db.DateTime, nullable=False)