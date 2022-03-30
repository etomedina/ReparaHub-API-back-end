"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
import json
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_jwt_extended  import JWTManager,create_access_token, get_jwt_identity, jwt_required


#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']= os.environ.get('FLASK_API_KEY')
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt=JWTManager(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed

@app.route('/registro_usuario/', methods=['POST'])
def registro_usuario():
    dictionary={}
    body = request.json
    user_email=body["email"],
    exists = db.session.query(User.email).filter_by(email=user_email).first() is not None 
    if exists:
        return jsonify({"msg":f"The email:{user_email} already exist in database, please add another user_email"}),400
    else:
        user = User.create(
            email=body["email"],
            password=body["password"],
            name=body["name"],
            familyname=body["familyname"]
             )
        dictionary = user.serialize()
        ##return jsonify(decoded_object), 201
        return jsonify(dictionary), 201       



@app.route('/login', methods=['POST'])
def login_user():
    body=request.json
    user_login=User.login(
        body["email"],body["password"]
    )
    if user_login:
        access_token=create_access_token(identity=user_login.id)
        print (access_token)
        return jsonify({ "token": access_token, "user_id": user_login.id }),201
        ##return jsonify(access_token),201  #201 de create
    else:
        return jsonify({"msg":"Please check your data, there are some mistake"}),400 

@app.route("/private", methods=["GET"])
@jwt_required()
def protected():
    user_id=get_jwt_identity()
    user=User.query.get(user_id)
    return jsonify(user.serialize()),200



if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
