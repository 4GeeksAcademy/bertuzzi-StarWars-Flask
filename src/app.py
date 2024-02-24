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
from models import db, Users
#from models import Person

# Flask instance
app = Flask(__name__)
app.url_map.strict_slashes = False
#Configure db (database)
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

@app.route('/users', methods=['GET','POST'])
def handle_users():
    response_body = results = {}
    if request.method == 'GET':
        # Here we add logic to consult database db and return all the users from the database
        # .scalars() returns an array of SQLAlchemy objects, whilst .scalar() returns a dictionary
        users = db.session.execute(db.select(Users)).scalars()
        results['users'] = [row.serialize() for row in users]
        response_body['result_users'] = results['users']
        response_body['message'] = 'GET method invoked'
        return response_body,200
    elif request.method == 'POST':
        # First we need to receive the data from the front to put in the object (we need to use .json method to make it readable from the backend)
        data = request.json
        ## data is an object that represents what has been sent on the request (in this case email,password)
        # Need to get the body from the frontend
        # Create an instance of the class Users (here we create a user with fixed values that we define by ourselves)
        # Here we now complete the new instance values with the key-value pairs of the request body
        user = Users(email = data['email'],
                    password = data['password'],
                    is_active = True)
        db.session.add(user)
        # Upon creating a user and committing the change, in this case we have an autoincremental id, so we do not need to create an id on our side
        db.session.commit()
        # Need to add .serialialize() because we need to return a value that is readable to the human eye (the serialize method is defined within the class in the models)
        response_body['result_user'] = user.serialize()
        response_body['message'] = 'POST method invoked'
        return response_body,200

# In this case we need to get a single user and therefore we need to modifiy the route to include the id that we send
@app.route('/user/<int:id>',methods=['GET'])
def handle_user(id):
    response_body = {}
    if request.method == 'GET':
        print(id)
        response_body['message'] = 'GET request of user ' + str(id)
        return response_body, 200
    if request.method == 'PUT':
        print(id)
        response_body['message'] = 'GET request of user ' + str(id)
        return response_body, 200
    if request.method == 'DELETE':
        # Logically speaking, if the user is DELETED we do not need to delete it, but we need to put the user as inactive otherwise there are gonna be inconsistencies with the database tables (is_active=False)
        print(id)
        response_body['message'] = 'GET request of user ' + str(id)
        return response_body, 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
