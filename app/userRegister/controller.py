from app import mongo
import bcrypt
def insert_user(user_detail):
    try:
        """here query_to_insert_user_in_db.acknowledged gives
           status which is boolean value.
         """
        email = user_detail['email']
        # print(email)
        find_email= mongo.db.user.find_one({'email':email})
        print("This is find",find_email)
        # print(find_email)
        if not find_email:
            status=mongo.db.users.insert_one(user_detail)

            result = True if status.acknowledged else False
            return result
        else:
            return False
    except Exception as e:
        return str(e)

"""This code is to test insert_user fucntion"""
# test_data = {"email" :"Amit pandey", "passsword": "djnfjsdnfa"}
# print(insert_user(test_data))

def find_user(user_details):
    try:
        result = mongo.db.users.find_one(user_details)

        if result:
            print("True of finduser2")
            return True
        else:
            print("True of finduser2")
            return False
    except Exception as e:
        return str(e)


def find_email(email_obj):
    try:
        result = mongo.db.users.find_one(email_obj)
        # print(result["email"],email_obj["email"])
        if result["email"] == email_obj["email"]:
            # print("True of finduser2")
            return True
        else:
            # print("True of finduser2")
            return False
    except Exception as e:
        return str(e)

#testing find_email
# email= {"email":"pamit1687@gmail.com"}
# print(find_email({"email":"pamit1687@gmail.com"}))

def update_is_verify(email_object):
    try:
        set_field ={"$set":{"is_verify":True}}
        query_to_update_is_verify = mongo.db.users.update_one(email_object,set_field)
        # print(query_to_update_is_verify,"dfasdjngs",query_to_update_is_verify.acknowledged)
        result = True if query_to_update_is_verify.acknowledged else False
        return result
    except Exception as e:
        return str(e)
# email = {"username":"Amit"}
# update_field = {"is_verify":True}
# print(update_is_verify(email,update_field))

def find_password(user_email,user_password):
    try:
        result = mongo.db.users.find_one(user_email)
        print(result["email"],user_email["email"])
        if result["email"] == user_email["email"]:
            # if result["password"] == user_email_password["password"]:
            if bcrypt.checkpw(user_password["password"],result["password"]):
                return True
            else:
                return False

        else:
            print("True of finduser2")
            return False
    except Exception as e:
        return str(e)
"""test data to test find_password"""
# user_details = {"email" : "pamit1687@gmail.com","password" : "password"}
# print(find_password(user_details))

def find_is_active(user_email_password):
    try:
        result = mongo.db.users.find_one(user_email_password)
        # print(result["email"],user_email_password["email"])
        result_ = True if result["is_verify"] else False
        return result_
        # if result["is_verify"] :
        #
        #     return True
        #
        # else:
        #
        #     return False
    except Exception as e:
        return str(e)
"""Testing this function """
# user_details = {"username" : "Amit4444","password" : "password"}
# print(find_is_active(user_details))

def get_role(user_info):
    try:
        porjection = {"role":1,"_id":0}
        result = mongo.db.users.find_one(user_info,porjection)
        # print(result["email"],user_email_password["email"])

        if result :
            return result['role']

        else:
            return "Please check your role acces"
    except Exception as e:
        return str(e)

# """Testing of get_role"""
# user_info = {"email" : "pamit1687@gmail.com","password" : "password"}
# print(get_role(user_info))

def update_password(email_obj,password_obj):
    try:
        set_query = {"$set":password_obj}
        query_to_update = mongo.db.users.update_one(email_obj,set_query)
        result = True if query_to_update.acknowledged else False
        return result
    except Exception as e:
        return str(e)
"""test this input """
# obj_email = {"email":"pamit1687@gmal.com", "password":"newpassword"}
# obj_to_update = {"password":"newpassword1"}
# print(update_password(obj_email,obj_to_update))
def update_isverify(email_obj,obj_isverify):
    try:
        set_query = {"$set":obj_isverify}
        query_to_update = mongo.db.users.update_one(email_obj,set_query)
        result = True if query_to_update.acknowledged else False
        return True
    except Exception as e:
        return str(e)

def get_pasword_bcrypt(email):
    query_to_find_userobj = mongo.db.users.find_one(email)
    return query_to_find_userobj['password']

# print(get_pasword_bcrypt(({"email":"pamit1687@gmail.com"})))