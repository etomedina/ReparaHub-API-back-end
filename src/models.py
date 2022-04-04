import email
from flask import render_template_string
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Base(db.Model):
    __abstract__=True
    created=db.Column(db.DateTime(timezone=True), default=db.func.now())
    updated=db.Column(db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now())

        
        

    def __init__(self, **kwargs): # keyword arguments
        """
        kwargs = {
        "name": "Luke",
        "eye_color": "brown",
        ...
        }
        """
        for (key, value) in kwargs.items(): #
            if key in ('created', 'updated'): continue
            if hasattr(self, key): #
                attribute_type = getattr(self.__class__, key).type
                try:
                    attribute_type.python_type(value)
                    setattr(self, key, value)
                except Exception as error:
                     print("ignoring key ", key, " with ", value, " for ", attribute_type.python_type, " because ", error.args)

    @classmethod
    def create(cls, **data):
        # crear la instancia
        instance = cls(**data)
        if (not isinstance(instance, cls)):
            print("FALLA EL CONSTRUCTOR")
            return None
        # guardar en bdd
        db.session.add(instance)
        try:
            ##Cambio de tulio es el existe valiadtion
            db.session.commit()
            print(f"created: {instance.id}")
            return instance
        except Exception as error:
            db.session.rollback()
            #return jsonify({"msg":f"The id alreade exist in database{User.id}, please add another id"})
            raise Exception(error.args) 

class User(Base):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name=db.Column(db.String(120))
    familyname=db.Column(db.String(120))
    telephone=db.Column(db.String(30))
    accesses = db.relationship('Incident', backref='user', lazy=True)
    vehicleses = db.relationship('Vehicle', backref='user', lazy=True)



    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email":self.email,
            "name":self.name,
            "telephone":self.telephone,
            "familyname":self.familyname
            # do not serialize the password, its a security breach
        }
    @classmethod
    def login(cls,email1,password):
        user=cls.query.filter_by(email=email1).one_or_none()
        if (not isinstance(user,cls)):
            return user
        if user.password==password:
            return user
        else:
            return False           

class Incident(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(240))
    coordinate=db.Column(db.String(100))
    rating=db.Column(db.String(100))
    status=db.Column(db.String(90))
    picture_incident =db.Column(db.String(240))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    trackings = db.relationship('Tracking', backref='user', lazy=True)
    provider_id=db.Column(db.Integer, db.ForeignKey('provider.id', ondelete="CASCADE"), nullable=False)        
   
    provider = db.relationship("Provider", back_populates="incident", uselist=False)
      
    def __repr__(self):
        return f" {self.id},{self.name},{self.coordinate}"    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "coordinate": self.coordinate,
            "rating": self.rating,
            "status": self.status,
            "picture_incident": self.picture_incident,
            "acces_id":self.acces_id
            # do not serialize the password, its a security breach
        }

class Tracking(Base):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(200))
    comments = db.Column(db.String(240))
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id', ondelete="CASCADE"), nullable=False)
   
    def __repr__(self):
        return f" {self.user_id},{self.comments},{self.incident_id}"    

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "comments": self.comments,
            "incident_id": self.incident_id
            # do not serialize the password, its a security breach
        }

class Provider(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(240))
    coordinate=db.Column(db.String(100))
    category=db.Column(db.String(100))
    rating=db.Column(db.String(90))
    incident = db.relationship("Incident", back_populates="provider")

  
    def __repr__(self):
        return f" {self.id},{self.name},{self.coordinate}"    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "coordinate": self.coordinate,
            "category": self.category,
            "rating": self.rating
            # do not serialize the password, its a security breach
        }

class Vehicle(Base):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(150))
    model = db.Column(db.String(240))
    category=db.Column(db.String(200))
    year=db.Column(db.String(50))
    transmision=db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
   
  
    def __repr__(self):
        return f" {self.id},{self.make},{self.model}"    
    def serialize(self):
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "category": self.category,
            "year": self.year,
            "transmision": self.transmision,
            "user_id":self.user_id
            
            # do not serialize the password, its a security breach
        }

