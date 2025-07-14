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
    college_courses = db.relationship('CollegeCourse', back_populates='college', lazy=True)

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
    college_course = db.relationship( # TODO: Change this to many-to-many relationship in future.
        "CollegeCourse",
        back_populates="faculty",
        # uselist=False,
        primaryjoin="Faculty.id==CollegeCourse.faculty_id"
    )

class Student(db.Model):
    """
    Represents a student enrolled in a college, storing personal and contact information, and linking to their quiz records.
    """
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)  # each student belongs to one college
    name = db.Column(db.String(100), nullable=False)
    personal_email = db.Column(db.String(255), unique=True, nullable=True) # ASK: personal or official ?
    contact_number = db.Column(db.String(15), unique=True, nullable=True)

    # RELATIONSHIPS
    college = db.relationship('College', back_populates='students') # each student belongs to one college
    enrollments = db.relationship('StudentCourseEnrollment', back_populates='student', lazy=True)

class YearTerm(db.Model):
    """
    Represents an academic year and term (e.g., 2024, t1), used to organize course offerings and records by time period.
    """
    __tablename__ = 'year_term'
    year = db.Column(db.String(4), primary_key=True)
    term = db.Column(db.String(2), primary_key=True)  # 't1', 't2', 't3'
    """Whenever you add a new year (e.g., 2025), you should insert three rows into the year_term table:
    for term in ['t1', 't2', 't3']:
        db.session.add(YearTerm(year='2025', term=term))
    db.session.commit()
    """

class CoreCourse(db.Model):
    """
    Represents a core course offered in the program, including its code, name, and credit value.
    """
    __tablename__ = 'core_courses'
    code = db.Column(db.String(10), primary_key=True) # course_code e.g ML-301, CS-301, etc.
    name = db.Column(db.String(255), nullable=False)
    credits = db.Column(db.Integer, nullable=False) # Some courses have 3 credits, some have 4 credits, etc.

    # RELATIONSHIPS
    college_courses = db.relationship('CollegeCourse', back_populates='course', lazy=True)
    
class CollegeCourse(db.Model): # This is a complex code. We will simplify if if needed while making the APIs.
    """
    This table is used to store the courses that are offered by a college in a particular year and term, and taught by specific faculty/faculties.
    """
    __tablename__ = 'college_courses'
    course_code = db.Column(db.String(10), db.ForeignKey('core_courses.code'), primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), primary_key=True)
    year = db.Column(db.String(4), primary_key=True)
    term = db.Column(db.String(2), primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=True)  # Nullable if course can be taught without faculty
    

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['year', 'term'],
            ['year_term.year', 'year_term.term']
        ),
    ) # This line creates a composite foreign key — meaning it links two columns together (year and term) in the CollegeCourse table to two columns in another table (YearTerm). This ensures that any (year, term) combination used in CollegeCourse must exist in YearTerm.

    # Relationships (optional but recommended)
    course = db.relationship('CoreCourse', back_populates='college_courses')
    college = db.relationship('College', back_populates='college_courses')
    year_term = db.relationship('YearTerm', primaryjoin="and_(CollegeCourse.year==YearTerm.year, CollegeCourse.term==YearTerm.term)")
    faculty = db.relationship('Faculty', back_populates='college_course')
    enrollments = db.relationship('StudentCourseEnrollment', back_populates='college_course', lazy=True)

class StudentCourseEnrollment(db.Model): # ASK: Based on the student and course-enrollment tables, I am thinking why can't we only have the course-enrollment table? There seems to be no question about the students that cannot be answered from course-enrollment table only.
    # TODO: Replace this table with "StudentCourse" table 
    """
    Represents the enrollment of a student in a specific course offering (CollegeCourse) for a given year and term.
    """
    __tablename__ = 'student_course_enrollments'
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    # student_email = db.Column(db.String(255), nullable=False) # TODO: Redundant info, remove later in schema if we are keeping the student table.
    course_code = db.Column(db.String(10), primary_key=True)
    # course_name = db.Column(db.String(255), nullable=False)
    college_id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(4), primary_key=True)
    term = db.Column(db.String(2), primary_key=True)
    completion_status = db.Column(db.String(20), nullable=False, default='in_progress')  # e.g., 'in_progress', 'completed', 'dropped'; NOTE: Hall ticket is NOT to be generated for dropped courses
    fee_payment_status = db.Column(db.String(20), nullable=False, default='unpaid')  # e.g., 'paid', 'unpaid', 'refunded in case of drop'; NOTE: This field will be same for all unique primary_keys, because a student pays combined fees for all courses that he wants to enroll.

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['course_code', 'college_id', 'year', 'term'],
            ['college_courses.course_code', 'college_courses.college_id', 'college_courses.year', 'college_courses.term']
        ),
    )

    # Relationships
    student = db.relationship('Student', back_populates='enrollments')
    college_course = db.relationship('CollegeCourse', back_populates='enrollments')
    quizzes = db.relationship('Quiz', back_populates='enrollment', lazy=True)

class Quiz(db.Model): # TODO: REPLACE WITH STUDENT MARKS
    """
    Represents a student's marks for a specific quiz or assessment in a particular course enrollment.
    Each record corresponds to one student's performance in one instance of a course offering.
    """
    __tablename__ = 'quizzes'
    enrollment_student_id = db.Column(db.Integer, primary_key=True) # student_course_enrollments.student_id
    enrollment_course_code = db.Column(db.String(10), primary_key=True) # student_course_enrollments.course_code
    enrollment_college_id = db.Column(db.Integer, primary_key=True) #TODO: Introduces some redundancy; can we directly provide the college_id from student_id without explictly specifying everytime?
    enrollment_year = db.Column(db.String(4), primary_key=True)
    enrollment_term = db.Column(db.String(2), primary_key=True)
    

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['enrollment_student_id', 'enrollment_course_code', 'enrollment_college_id', 'enrollment_year', 'enrollment_term'],
            ['student_course_enrollments.student_id', 'student_course_enrollments.course_code', 'student_course_enrollments.college_id', 'student_course_enrollments.year', 'student_course_enrollments.term']
        ),
    )

    # Marks columns (all nullable)
    quiz_1 = db.Column(db.Float, nullable=True)
    quiz_2 = db.Column(db.Float, nullable=True)
    end_term = db.Column(db.Float, nullable=True)
    oppe1 = db.Column(db.Float, nullable=True)
    oppe2 = db.Column(db.Float, nullable=True)
    nppe1 = db.Column(db.Float, nullable=True)
    nppe2 = db.Column(db.Float, nullable=True)

    quiz_1_hall_ticket_url = db.Column(db.String(255), nullable=True)  # URL to the quiz 1 hall ticket
    quiz_2_hall_ticket_url = db.Column(db.String(255), nullable=True) # URL to the quiz 2 hall ticket
    end_term_hall_ticket_FN_url = db.Column(db.String(255), nullable=True)  # URL to the end term hall ticket of Forenoon FN session
    end_term_hall_ticket_AN_url = db.Column(db.String(255), nullable=True)  # URL to the end term hall ticket of Afternoon AN session

    # Relationships
    enrollment = db.relationship('StudentCourseEnrollment', back_populates='quizzes')