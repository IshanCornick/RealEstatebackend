from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api, Resource
from __init__ import app, db, cors
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model.reviews import Review
# from auth_middleware import token_required


review_api = Blueprint('review_api', __name__, url_prefix='/api/review')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(review_api)


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
# db = SQLAlchemy(app)


class ReviewAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            rating = body.get('rating')
            comment = body.get('comment')
            # userid = body.get("userid")
            
            ''' #1: Key code block, setup USER OBJECT '''
            review = Review(
                        rating=rating,
                        comment=comment
                        )


            ''' #2: Key Code block to add user to database '''
            # create user in database
            review = review.create()
            # success returns json of user
            if review:
                return jsonify(review.read())

            # failure returns error
            return {'message': f'Error processing request'}, 400

        # this method is when users click on specific job(say "IT Help"), and it will return information about it
        def get(self): # Read Method
            
                reviews = Review.query.all()    # read/extract all users from database
                json_ready = [review.read() for review in reviews]  # prepare output in json
                return jsonify(json_ready) # jsonify creates Flask response object, more specific to APIs than json.dump 
            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')