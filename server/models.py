from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db


# ================== USER ===================== #

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String, nullable=False)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False) 

    pins = db.relationship('Pin', back_populates='user')
    plant = association_proxy('pins', 'plant')
    serialize_rules = ('-pins.user')

    def __repr__(self):
        return f'User obj{self.id}: name:{self.fname} {self.lname}, username:{self.username}, address:{self.address}, pins:{self.pins}'

# ================== PIN ===================== #

class Pin(db.Model, SerializerMixin):
    __tablename__ = 'pins'
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    # check if geometry tracks coordinates
    location = db.Column(db.String, nullable=False) 
    comment = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'))

    user = db.relationship('User', back_populates='pins')
    plant = db.relationship('Plant', back_populates='pins')
    serialize_rules = ('-user.pins', '-plant.pins')

    def __repr__(self):
        return f'Pin obj{self.id}: location:{self.location}, contributed by:{self.user_id}, for plant:{self.plant_id}'

# ================== PLANT ===================== #

class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    plant_name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, unique=True)

    pins = db.relationship('Pin', back_populates='plant')
    user = association_proxy('pins', 'user')
    serialize_rules = ('-pins.plant')

    def __repr__(self):
        return f'Plant obj{self.id}: plant_name:{self.plant_name}, img:{self.image}, pins:{self.pins}'