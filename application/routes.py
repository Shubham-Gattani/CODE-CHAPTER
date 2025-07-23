# This file will contain the routes of our application, that we may or may not use in our application.

import random
from datetime import datetime, timedelta
from flask_mail import Message
from flask import current_app as app, jsonify, request, render_template
from flask_security import auth_required, roles_required, roles_accepted, current_user, login_user, hash_password, verify_password

# IMPORTS FROM OTHER FILES
from .database import db
from .models_6 import User, SpocDetails, Student, OTP

# Once our backend is ready, we will try to connect to the frontend. Since we are using CDN, so we will need a starting point, this route will act as the starting point which will load index.html on which our Vue script will run.
@app.route("/", methods=["GET"]) # This is the home page. It will have some images and a LOGIN BUTTON. Clicking on LOGIN, a login page/form should be shown with a SUBMIT button, which should send a POST to /api/login, and if the LOGIN is successful, we should be redirected to SPOC dashboard
def home():
    # return render_template("test.html")
    return render_template("index.html")

@app.route('/api/login', methods=['POST'])
def user_login():
    body = request.get_json()
    email = body['email']
    password = body['password']
    print(f"DATA RECIEVED FROM FRONTEND: {email}")

    if not email:
        return jsonify({
            "message": "Email is required!"
        }), 400
    
    user = app.security.datastore.find_user(email = email)

    if user:
        if verify_password(password, user.password):
            
            # if current_user is not None:
            #     return jsonify({
            #     "message": "Already logged in!"
            # }), 400
            login_user(user) # This will set the current_user to the user object, and also set the session cookie in the browser.
            print(current_user)
            return jsonify({
                "id": user.id,
                # "email": user.email,
                "role": user.role,
                "auth_token": user.get_auth_token(),
                # "roles": roles_list(user.roles) 
                # "roles": roles_list(current_user.roles) 
            })
        else: # password hash doesn't match
            return jsonify({
                "message": "Incorrect Password"
            }), 400
    else: # user with this email doesn't exist
       return jsonify({
            "message": "User Not Found!"
        }), 404
    
# SPOC DASHBOARD APIs
@app.get("/api/spoc_dashboard/college_details")
@auth_required("token")
def get_college_details_for_spoc_dashboard():
    if current_user.role != "spoc":
        return jsonify({"error": "Unauthorized"}), 403
    spoc = current_user.spoc # (current_user.spoc) DIRECTLY gives the 1-1 related SPOC object
    if not spoc:
        return jsonify({"error": "SPOC not found"}), 404

    # College details
    college = spoc.college
    if college:
        return jsonify({
            "cc_id": college.cc_id,
            "college_name": college.college_name,
            "logo_path": college.logo_path,
            "addr1": college.addr1,
            "aicte_approved": college.aicte_approved,
            "city": college.city,
            "pincode": college.pincode,
            "college_link": college.college_link,
            "university": college.university,
            "mobile_no1": college.mobile_no1,
            "mobile_no2": college.mobile_no2,
            "partnering_since": college.partnering_since,
            "updated_at": college.updated_at,
            "is_active": college.is_active,
            "state": college.stateName,
            "country": college.country,
            "instituteType": college.instituteType,
            "timestamp": college.timestamp,
            "updated_by": college.updated_by,
            "changes": college.changes,
            "mou_cloud_link": college.mou_cloud_link,
            "mou_grive_link": college.mou_grive_link
        }), 200

    else:
        return jsonify({"error": "College not found"}), 404

@app.get("/api/spoc_dashboard/spoc_details")
@auth_required("token")
def get_spoc_details_for_spoc_dashboard():
    if current_user.role != "spoc":
        return jsonify({"error": "Unauthorized"}), 403
    spoc = current_user.spoc
    if not spoc:
        return jsonify({"error": "SPOC not found"}), 404

    # SPOC details
    spoc_data = {
        "id": spoc.id,
        "user_id": spoc.user_id,
        "spoc_name": spoc.spocName,
        "spoc_emailid": spoc.spoc_emailid,
        "principal_name": spoc.principal_name,
        "principal_email": spoc.principal_email,
        "principal_mobile": spoc.principal_mobile,
        "designation": spoc.designation,
        "department": spoc.department,
        "mobile_number_1": spoc.mobileNumber,
        "mobile_number_2": spoc.mobileNumber2,
        "profile_photo": spoc.profile_photo,
        "updated_at": spoc.updated_at,
        "college_id": spoc.cc_id,
        "college_name": spoc.college.college_name if spoc.college else None,
        "status": spoc.status,
        "spoc_onboard": spoc.spoc_onboard
        }


    return jsonify(spoc_data), 200

@app.get("/api/spoc_dashboard/mou")
@auth_required("token")
def get_mou_pdf():
    # spoc = current_user.spoc # TODO: MoU is a feature of college and not the SPOC. We will change this later.
    # if not spoc:
    #     return jsonify({"error": "SPOC not found"}), 404

    filename = "https://drive.google.com/file/d/1rrGrsGwCBQerBpRG8TH0wci1RdhB6muD/view?usp=drive_link"
    return jsonify({"path": filename}), 200


@app.get("/api/spoc_dashboard/student_details")
@auth_required("token")
def get_student_details_for_spoc_dashboard():
    if current_user.role != "spoc":
        return jsonify({"error": "Unauthorized"}), 403
    
    spoc = current_user.spoc
    if not spoc or not spoc.college:
        return jsonify({"error": "SPOC or College not found"}), 404
    
    students = Student.query.filter_by(college_id=spoc.college.id).all()
    student_list = [
        {
            "id": s.id,
            "college_id": s.college_id,
            "college_name": s.college.college_name if s.college else None,
            "name": s.name,
            "personal_email": s.personal_email,
            "contact_number": s.contact_number,
            "dob": s.dob,
            "profile_photo": s.profile_photo,
            "signature": s.signature,
            "id_card": s.id_card
        } for s in students
    ]
    return jsonify({"students": student_list}), 200

@app.route('/api/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"message": "Email is required"}), 400

    user = app.security.datastore.find_user(email=email)
    if not user:
        return jsonify({"message": "User not found"}), 404

    otp_code = str(random.randint(100000, 999999))
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    # Save OTP to DB
    otp_entry = OTP(email=email, otp=otp_code, expires_at=expires_at)
    db.session.add(otp_entry)
    db.session.commit()

    # Send OTP via email
    msg = Message("Your OTP Code", recipients=[email])
    msg.body = f"Your OTP code is: {otp_code}"
    app.mail.send(msg)

    return jsonify({"message": "OTP sent"}), 200

@app.route('/api/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp_code = data.get('otp')

    otp_entry = OTP.query.filter_by(email=email, otp=otp_code).order_by(OTP.created_at.desc()).first()
    if not otp_entry or otp_entry.expires_at < datetime.utcnow():
        return jsonify({"message": "Invalid or expired OTP"}), 400

    # Optionally, delete OTP after use
    db.session.delete(otp_entry)
    db.session.commit()

    user = app.security.datastore.find_user(email=email)
    login_user(user)
    return jsonify({
        "id": user.id,
        "role": user.role,
        "auth_token": user.get_auth_token(),
    }), 200




















