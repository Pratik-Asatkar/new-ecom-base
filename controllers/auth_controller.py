from flask import Blueprint, render_template, request, make_response, redirect
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

import models.user as user_dbs
import tools.utils as utils

auth = Blueprint('auth', __name__, template_folder="templates")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        passwd = request.form.get('passwd')
        username = email.split('@')[0].strip()

        user_data = user_dbs.get_user_details(username)
        
        if user_data:
            # authenticate user
            if passwd == user_data['passwd']:
                # user auth success

                payload = {
                    "sub": username,
                    "iat": utils.current_epoch()
                }

                access_token = create_access_token(identity=payload)
                resp = make_response(redirect('/'))
                resp.set_cookie('access_token_cookie', access_token)

                print(f"{username} successfully logged-in")
                return resp
        print(f"{username} failed to login, password: {passwd}")
        return render_template('login.html', err="Incorrect Username/Password!")


@auth.route('/logout')
@jwt_required(locations='cookies')
def logout():
    user = get_jwt_identity()

    resp = make_response(redirect('/'))
    resp.set_cookie('access_token_cookie', '', expires=0)

    print(f"{user['sub']} has successfully logged out!")

    return resp


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('email').split('@')[0].strip()

        data = {
            "_id": username,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "passwd": request.form.get('passwd'),
            "address": request.form.get('address'),
            "pincode": request.form.get('pincode'),
            "cart": {
                "cartid": utils.get_cart_id(),
                "total": 0,
                "items": {}
            },
            "previous_orders": []
        }

        if user_dbs.register(data):
            print(f"{username} have successfully registered!")
            return redirect('/auth/login')
        else:
            print(f"{username} couldn't register!")
            return render_template('login.html', err="You already have account with us, kindly login!")

