from flask import Flask, make_response, jsonify, request, Blueprint
from flask_restful import Resource, Api
from app.userRegister.controller import insert_user, find_user, find_email, update_is_verify, find_password, \
    find_is_active, get_role, update_password, update_isverify, get_pasword_bcrypt
from app.userRegister.verification import Verification, emailVerification
from app import api, mongo
from app import mail
from flask_mail import Message
import jwt
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import bcrypt
from celery import shared_task
from app import mail
from flask_mail import Message
from app.celery_config.celery_task import *

example_blueprint = Blueprint("example_blueprint", __name__)


class UserRegistration(Resource):
    def post(self):
        try:
            email = request.json.get("email", "NA")
            print("This is email", email)
            password = request.json.get("password", "NA").encode('ASCII')
            print("This is line 16", email, password)
            role = request.json.get("role", "admin")
            is_verify = False
            encode_password = bcrypt.hashpw(password, bcrypt.gensalt())

            # Checking if email/password  is empty
            verify_obj = Verification()
            result = verify_obj.verify_email_password(email, password)
            if result != "Valid email password":
                return make_response(jsonify({"message": result}))

            # checking if emailid entred is correct
            object_of_email_verification = emailVerification()
            result_of_valid_email = object_of_email_verification.verfy_email(email)
            if not result_of_valid_email:
                return make_response(jsonify({"message": "Invalid Email"}))
            ######################################

            details_of_user = {"email": email, "password": password, "role": role, "is_verify": is_verify}
            print("This is test for db")
            results = insert_user(details_of_user)
            print("THIS IS RESULT",results)
            print("This is of views results status: ", results)
            """Setting expire time for verification tokken """
            expire_token_time = datetime.now() + timedelta(minutes=15)
            expire_epoch_time = int(expire_token_time.timestamp())
            details_to_make_jwt_tokken = {"email": email, "exp": expire_epoch_time}

            veryfication_tokken = jwt.encode(details_to_make_jwt_tokken, "amit", algorithm="HS256")

            if results == True:
                result_from_task = send_mail.apply_async(args=[email, veryfication_tokken],countdown=3)
                # print("line1")
                # msg = Message('Testing', sender='ap7788546@gmail.com', recipients=[email])
                # print("line2")
                # msg.body = f"This is your verification Token: {veryfication_tokken}"
                # print("line 3")
                # msg.html =f"<h1><a href='http://0.0.0.0:80/v1/api/verifyEmail?token={veryfication_tokken}'>Click on link to verify</a></h1>"
                # print("line 4")
                # mail.send(msg)
                # print("line 5")
                return make_response(jsonify({"message": "please check your mail for verification tokken"}))
            return make_response(jsonify({"message": "Partial"}))
            ######################################
        except Exception as e:
            return make_response(jsonify({"message": f"str{e}"}))

    # @shared_task(ignore_result=False)
    # def send_mail(email, veryfication_tokken):
    #     msg = Message('Testing', sender='ap7788546@gmail.com', recipients=[email])
    #     print("line2")
    #     msg.body = f"This is your verification Token: {veryfication_tokken}"
    #     print("line 3")
    #     msg.html = f"<h1><a href='http://0.0.0.0:80/v1/api/verifyEmail?token={veryfication_tokken}'>Click on link to verify</a></h1>"
    #     print("line 4")
    #     mail.send(msg)
    #     print("line 5")
    #     print(True)


class verifyEmail(Resource):

    def get(self):
        try:
            # token = request.json.get('token')
            token = request.args.get('token')

            if token in ["NA", ""]:
                return make_response(jsonify({"message": "Yon have not entred your token"}))
            # veryfication_tokken = jwt.encode(details_to_make_jwt_tokken,"amit",algorithm="HS256")

            decrpt_token = jwt.decode(token, "amit", algorithms=["HS256"])
            data_for_query = {"email": decrpt_token['email']}
            result_of_find = find_email(data_for_query)
            if result_of_find == True:
                update_query = update_is_verify(data_for_query)
                try:
                    if update_query:
                        return make_response(jsonify({"message": "Sucessful Verified!"}))
                    else:
                        return make_response(jsonify({"message": "Failed to update"}))
                except Exception as e:
                    return make_response(jsonify({"message": str(e)}))

        except Exception as e:
            return str(e)


class Login(Resource):
    def post(self):
        try:
            email = request.json.get("email", "NA")
            password = request.json.get("password", "NA").encode()

            if email in ["NA", ""] or password in ["NA", ""]:
                return make_response(jsonify({"message": "Please Enter Correct Mail and password"}))
            else:
                user_details = {"email": email}
                find_user_details = find_user(user_details)
                find_user_active = find_is_active(user_details)
                if find_user_active:
                    if find_user_details:
                        password_obj = {"password": password}
                        find_pass = find_password(user_details, password_obj)
                        print("this is find_pass", find_pass)
                        if find_pass:
                            claims = {"role": get_role(user_details)}
                            access_token = create_access_token(identity=email)
                            refresh_token = create_refresh_token(identity=email)
                            return make_response(jsonify({"acces-token": access_token, "refresh-token": refresh_token}))

                        else:
                            return make_response(jsonify({"message": "You have Entred Incorrect Password!"}))



                    else:
                        return make_response(jsonify({"message": "Please Check your mail its and incorrect!"}))
                else:
                    return make_response(jsonify({"message": "Please verify your account!!"}))
        except Exception as e:
            return make_response(jsonify({"message": str(e)}))


class UpdateData(Resource):
    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        user_role = get_role({"email": email})
        find_mail = find_email({"email": email})
        if user_role:
            if find_mail:

                # field_to_update = request.json.get("age","NA")
                current_password = request.json.get("current_password", "NA").encode()
                new_password = request.json.get("new_password", "NA").encode()
                user_email = {"email": email}
                user_password = {"password": current_password}
                password_result = find_password(user_email, user_password)
                if new_password in ["NA", ""]:
                    return make_response(jsonify({"message": "Enter value to update!"}))
                else:
                    if password_result:
                        obj_email = {"email": email}
                        obj_to_update = {"password": new_password}
                        result = update_password(obj_email, obj_to_update)
                        if result:
                            return make_response(jsonify({"message": "Field has been Updated!!"}))
                        else:
                            return make_response(jsonify({"message": "Field has been not updated "}))
                    else:
                        return make_response(jsonify({"message": "Incorrect current passsword!"}))
            else:
                return make_response(jsonify({"message": "Your Email address is wrong"}))
        else:
            return make_response(jsonify({"message": "You are not allowed to update! Please update your pemissions"}))


class DeleteUser(Resource):
    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        user_role = get_role({"email": email})
        find_mail = find_email({"email": email})
        if user_role:
            if find_mail:
                obj_email = {"email": email}
                obj_isverify = {"is_verify": False}
                result = update_isverify(obj_email, obj_isverify)
                if result:
                    return make_response(jsonify({"message": "Users has been Deleted!!"}))
                else:
                    return make_response(jsonify({"message": "Users has been not updated "}))

            else:
                return make_response(jsonify({"message": "Your Email address is wrong"}))
        else:
            return make_response(jsonify({"message": "You are not allowed to update! Please update your pemissions"}))


class HealthCheck(Resource):
    def get(self):
        try:
            email = request.json.get("email")
            # result = mongo.db.user.insert_one({"email":email})
            print("health Check")
            return make_response(jsonify({"message": "This is health check"}))
        except Exception as e:
            return make_response(jsonify({"message": str(e)}))


class CeleryTask(Resource):
    def get(self):
        display.delay()
        # send_mail.delay(args=['pamit1687@gmail.com',"dfasdfbsdafbsd"],countdown=5)
        return make_response(jsonify({"mess":""}))


api.add_resource(UserRegistration, '/v1/api/register')
api.add_resource(verifyEmail, '/v1/api/verifyEmail')
api.add_resource(Login, '/v1/api/login')
api.add_resource(UpdateData, '/v1/api/update')
api.add_resource(DeleteUser, '/v1/api/delete')
api.add_resource(HealthCheck, "/v1/api/health")
api.add_resource(CeleryTask, "/")
