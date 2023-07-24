import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()


def make_celery(app):
    # celery = Celery(app.name, broker=os.getenv('RABBITMQ_URI'))
    # celery.conf.update(app.config)
    # celery.conf.accept_content = ["json", "pickle", "yaml"]

    celery_app = Celery(
        app,
        broker=os.getenv('RABBITMQ_URI'),
        include=['app.celery_config.celery_task']
    )
    with app.app_context():
        # Access any Flask application-specific functionality here

        print(app.config)
        celery_app.conf.update(
            app.config)
        celery_app.conf.accept_content = ["json", "yaml"]
    return celery_app
