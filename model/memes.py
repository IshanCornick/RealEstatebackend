from random import randrange
from datetime import datetime
import os
import base64
import json
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Text
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import app, db

class Image(db.Model):
    __tablename__ = 'Images'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    mimetype = db.Column(db.Text(100), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    upload_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __init__(self, filename, mimetype, image_data):
        self.filename = filename
        self.mimetype = mimetype
        self.image_data = image_data

    def __init__(self, filename, mimetype, image_data, upload_date):
        self.filename = filename
        self.mimetype = mimetype
        self.image_data = image_data
        self.upload_date = upload_date
 

    def __repr__(self):
        return f"Image(id={self.id}, filename={self.filename}, mimetype={self.mimetype})"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self): 
        return {
            "id": self.id,
            "filename": self.filename,
            "mimetype": self.mimetype,
            "upload_date": self.upload_date
        }


def initImages():
    with app.app_context():
        db.create_all()
        for _ in range(1):  # Create 1 image for testing
            try:
                filename = 'logo.png'
                mimetype = 'image/png'
                file_path = r"./volumes/uploads/ncs_logo.png"  # Use raw string literal or escape backslashes
                upload_date = datetime.now()

                #file_path = os.getcwd()  # Use raw string literal or escape backslashes
                print(os.getcwd())
                with open(file_path, 'rb') as f:
                    image_data = f.read()
                image = Image(filename=filename, mimetype=mimetype, image_data=image_data,upload_date=upload_date)
                image.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate email, or error")