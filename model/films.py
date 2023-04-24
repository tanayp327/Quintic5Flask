""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json
import pickle
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import PickleType
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table

class Films(db.Model):
    __tablename2__ = 'Films'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    _name = db.Column(db.String(255), primary_key=True, nullable=False)
    _year = db.Column(db.Integer, unique=False, nullable=False)
    _epcount = db.Column(db.Integer, unique=False, nullable=False)
    _language = db.Column(db.String(255), unique=False, nullable=False)
    _trailer = db.Column(db.String(255), unique = False, nullable=False)
    _eplist = db.Column(PickleType, unique = False, nullable=False)
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    #posts = db.relationship("Post2", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, year, epcount, language, trailer, eplist):
        self._trailer=trailer
        self._name = name
        self._epcount = epcount
        self._year = year
        self._language = language# variables with self prefix become part of the object, 
        self._eplist = eplist
    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def year(self):
        return self._year
    
    # a setter function, allows name to be updated after initial object creation
    @year.setter
    def year(self, year):
        self._year = year
       
    @property
    def language(self):
        return self._language
    
    # a setter function, allows name to be updated after initial object creation
    @language.setter
    def language(self, language):
        self._language = language

    @property
    def epcount(self):
        return self._epcount
    
    # a setter function, allows name to be updated after initial object creation
    @epcount.setter
    def epcount(self, epcount):
        self._epcount = epcount
        
    @property
    def trailer(self):
        return self._trailer
    
    # a setter function, allows name to be updated after initial object creation
    @trailer.setter
    def trailer(self, trailer):
        self._trailer = trailer
        
    @property
    def eplist(self):
        return self._eplist
    
    @eplist.setter
    def eplist(self, eplist):
        self._eplist = eplist
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        #try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        #except IntegrityError:
         #   db.session.remove()
          #  return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "name": self.name,
            "year": self.year,
            "language":self.language,
            "episode count": self.epcount,
            "episode list": self.eplist,
            "trailer link": self.trailer
        }
    #"posts": [post.read() for post in self.posts]
    # CRUD update: updates user name, password, phone
    # returns self

    def update(self, epwatched, neweplist):
        self._epcount += epwatched
        myeplist = self._eplist.copy() # create a copy of the eplist
        for i in neweplist:
            myeplist.append(i)
        self._eplist = myeplist
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return {"message":f"deleted {self}"}
"""Database Creation and Testing """


# Builds working data for testing
def initFilms():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    u1 = Films(name='test',year=0,epcount = 1,language="Chinmayan",trailer = "7huivfbhgvbhgbrgb4bvdghb",eplist = ["1","2"])

    films = [u1]

            