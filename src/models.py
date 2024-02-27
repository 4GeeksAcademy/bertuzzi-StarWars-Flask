from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    # Def allows us to represent 
    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
            # This is what we send to the front as a dictionary
            # The serialize method allows us give back the specific information we want to return to the front, for instance by means of an endpoint
        }

class Planet(db.Model):
    __tablename__='planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    population = db.Column(db.Integer,nullable=False)
    diameter = db.Column(db.Integer,nullable=False)
    climate = db.Column(db.String(50),nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Charachter(db.Model):
    __tablename__='characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    gender = db.Column(db.String(50),nullable=False)
    birth_year = db.Column(db.Integer,nullable=False)
    homeworld = db.Column(db.String(50),nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class FavoritePlanet(db.Model):
    __tablename__='favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    user = db.relationship('User',foreign_keys=[user_id])
    planet = db.relationship('Planet', foreign_keys=[planet_id])

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }

class FavoriteCharacter(db.Model):
    __tablename__='favorite_characters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    user = db.relationship('User',foreign_keys=[user_id])
    character = db.relationship('Charachter', foreign_keys=[character_id])

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }
