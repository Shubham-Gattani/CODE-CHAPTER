# This file will contain the routes of our application, that we may or may not use in our application.

from flask import current_app as app, jsonify, request, render_template
from flask_security import auth_required, roles_required, roles_accepted, current_user, login_user, hash_password, verify_password

# IMPORTS FROM OTHER FILES
from .database import db
from .models_4 import User, SPOC

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
    # spoc_id = current_user.spoc.id # (current_user.spoc) gives the 1-1 related SPOC object; and (current_user.spoc).id gives the required spoc_id
    spoc = current_user.spoc # (current_user.spoc) DIRECTLY gives the 1-1 related SPOC object
    # spoc = SPOC.query.get(spoc_id)
    if not spoc:
        return jsonify({"error": "SPOC not found"}), 404

    # College details
    college = spoc.college
    if college:
        return jsonify({
            "id": college.id,
            "name": college.name,
            "address": college.address,
            "city": college.city,
            "state": college.state,
            "pincode": college.pincode
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
        "name": spoc.name,
        "personal_email": spoc.personal_email,
        "designation": spoc.designation,
        "contact_number": spoc.contact_number,
        "user_id": spoc.user_id,
        "college_name": spoc.college.name,
        "user_email": spoc.user.email if spoc.user else None
    }

    return jsonify(spoc_data), 200

@app.get("/api/spoc_dashboard/mou")
@auth_required("token")
def get_mou_pdf():
    # spoc = current_user.spoc # TODO: MoU is a feature of college and not the SPOC. We will change this later.
    # if not spoc:
    #     return jsonify({"error": "SPOC not found"}), 404

    filename = f"ID card 2025.pdf"
    return jsonify({"path": f"/static/{filename}"}), 200

@app.get("/api/spoc_dashboard/request_letter")
@auth_required("token")
def get_request_letter_pdf():
    # spoc = current_user.spoc # TODO: MoU is a feature of college and not the SPOC. We will change this later.
    # if not spoc:
    #     return jsonify({"error": "SPOC not found"}), 404

    filename = f"ID card 2025.pdf"
    return jsonify({"path": f"/static/{filename}"}), 200























