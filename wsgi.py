from app.userRegister.views import example_blueprint
from flask import Blueprint
from flask_restful import Api
from app import app

app.register_blueprint(example_blueprint)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

