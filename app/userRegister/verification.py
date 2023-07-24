"""this module is been used to verify email and password"""
import re
class Verification:
    def verify_email_password(self,email,password):
        if email in ["NA",""]:
            return "Invalid email"
        elif password in ["NA",""]:
            return "Invalid password"
        else:
            return "Valid email password"
# email = "pamdjfbjsd"
# password = "dfasd"
# testobj = Verification()
# print(testobj.verify_Email_password(email,password))

class emailVerification:
    def verfy_email(self,email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

# test_object= emailVerification()
# print(test_object.verfy_email('fgdfgasdgfas@gmail.com'))


