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
from models import db, User,Charachter,Planet,FavoritePlanet,FavoriteCharacter
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

@app.route('/people', methods=['GET'])
def get_characters():
    response_body = results = {}
    characters = db.session.execute(db.select(Charachter)).scalars()
    results['characters'] = [row.serialize() for row in characters]
    response_body['res'] = results['characters']
    response_body['message'] = 'GET request for characters'
    print(response_body)
    return response_body,200

@app.route('/planets',methods=['GET'])
def get_planets():
    response_body = results = {}
    planets = db.session.execute(db.select(Planet)).scalars()
    results['planets'] = [row.serialize() for row in planets]
    response_body['res'] = results['planets']
    response_body['message'] = 'GET request for characters'
    print(response_body)
    return response_body,200

@app.route('/people/<int:id>',methods=['GET'])
def get_char(id):
    response_body = results = {}
    character = db.session.execute(db.select(Charachter).where(Charachter.id == id)).scalar()
    char = character.serialize()
    response_body['res'] = results['res'] = char
    response_body['message'] = results['message'] = 'GET request of character ' + str(id)
    return response_body,200

@app.route('/planets/<int:id>',methods=['GET'])
def get_plan(id):
    response_body = results = {}
    planet = db.session.execute(db.select(Planet).where(Planet.id == id)).scalar()
    plan = planet.serialize()
    response_body['res'] = results['res'] = plan
    response_body['message'] = results['message'] = 'GET request of planet ' + str(id)
    return response_body,200

@app.route('/users', methods=['GET'])
def get_users():
    response_body = results = {}
    users = db.session.execute(db.select(User)).scalars()
    results['users'] = [row.serialize() for row in users]
    response_body['res'] = results['users']
    response_body['message'] = 'GET request for users'
    return response_body,200

@app.route('/users/<int:id>/favorites',methods=['GET'])
def get_favorites(id):
    response_body = results = {}
    favorites = []
    favorite_characters = db.session.execute(db.select(FavoriteCharacter).where(FavoriteCharacter.user_id == id)).scalars()
    fav_char = [row.serialize() for row in favorite_characters]
    [favorites.append(char) for char in fav_char]
    favorite_planets = db.session.execute(db.select(FavoritePlanet).where(FavoritePlanet.user_id == id)).scalars()
    fav_plan = [row.serialize() for row in favorite_planets]
    [favorites.append(plan) for plan in fav_plan]
    response_body['res'] = results['res'] = favorites
    response_body['message'] = results['message'] = 'GET request for favorites of active users'
    return response_body,200

@app.route('/favorite/<int:id>/planets',methods=['POST'])
def handle_fav_planet(id):
    response_body = results = {}
    data = request.json
    favorite_planet = FavoritePlanet(
        user_id = id,
        planet_id = data['planet_id']
        )
    db.session.add(favorite_planet)
    db.session.commit()
    response_body['res'] = results['res'] = favorite_planet.serialize()
    response_body['message'] = results['message'] = 'Favorite planet added. Planet id: ' + str(data['planet_id'])
    return response_body,200

@app.route('/favorite/<int:user_id>/planets/<int:planet_id>',methods=['DELETE'])
def delete_fav_planet(user_id,planet_id):
    response_body = results = {}
    planet = db.session.execute(db.select(FavoritePlanet).where((FavoritePlanet.planet_id == planet_id )&(FavoritePlanet.user_id == user_id))).scalar()
    db.session.delete(planet)
    db.session.commit()
    favorites = db.session.execute(db.select(FavoritePlanet)).scalars()
    response_body['res'] = results['res'] = [row.serialize() for row in favorites]
    response_body['message'] = results['message'] = 'planet id number ' + str(planet_id) + ' deleted successfully!'
    return response_body,200

@app.route('/favorite/<int:id>/people',methods=['POST'])
def handle_fav_char(id):
    response_body = results = {}
    data = request.json
    favorite_character = FavoriteCharacter(
        user_id = id,
        character_id = data['character_id']
        )
    db.session.add(favorite_character)
    db.session.commit()
    response_body['res'] = results['res'] = favorite_character.serialize()
    response_body['message'] = results['message'] = 'Favorite character added. Character id: ' + str(data['character_id'])
    return response_body,200

@app.route('/favorite/<int:user_id>/people/<int:person_id>',methods=['DELETE'])
def delete_fav_char(user_id,person_id):
    response_body = results = {}
    character = db.session.execute(db.select(FavoriteCharacter).where((FavoriteCharacter.character_id == character_id )&(FavoriteCharacter.user_id == user_id))).scalar()
    db.session.delete(character)
    db.session.commit()
    favorites = db.session.execute(db.select(FavoriteCharacter)).scalars()
    response_body['res'] = results['res'] = [row.serialize() for row in favorites]
    response_body['message'] = results['message'] = 'character id number ' + str(person_id) + ' deleted successfully!'
    return response_body,200

    




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
