import io
import time
from flask_mail import Mail
from app import app
from app import mongo
from app.celery_config.make_celery import make_celery
from celery import shared_task
from app import mail
from flask_mail import Message
from app import celery,app

@celery.task()
def send_mail(email, veryfication_tokken):
    mail = Mail(app)
    with app.app_context():
        try:

            msg = Message('Testing', sender='ap7788546@gmail.com', recipients=[email])
            print("line2")
            msg.body = f"This is your verification Token: {veryfication_tokken}"
            print("line 3")
            msg.html = f"<h1><a href='http://0.0.0.0:80/v1/api/verifyEmail?token={veryfication_tokken}'>Click on link to verify</a></h1>"
            print("line 4")
            mail.send(msg)
            print("line 5")
            print(True)
        except Exception as e:
            print(str(e))

