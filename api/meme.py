from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource
from datetime import datetime
from auth_middleware import token_required
from model.memes import Image  # Assuming Image is the SQLAlchemy model for storing images
from flask import Flask
from flask_cors import CORS
from flask import send_file
import io
import random

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

# Define your API routes and other application setup

meme_api = Blueprint('meme_api', __name__, 
                     url_prefix='/api/memes')

api = Api(meme_api)

class ImageAPI:        
    class _CRUD(Resource):
        def put(self):
            try:
                body = request.get_json()
                image_id = body.get('id')
                filename = body.get('filename')
                mimetype = body.get('mimetype')
                image_data = body.get('image_data')
                if not all([image_id, filename, mimetype, image_data]):
                    return {'message': 'Missing required fields'}, 400
                image = Image.query.filter_by(id=image_id).first()
                if image:
                    image.update(filename, mimetype, image_data)
                    return jsonify(image.read())
                else:
                    return {'message': 'Image not found'}, 404
            except Exception as e:
                return {'message': str(e)}, 500

        def delete(self):
            try:
                image_id = request.args.get('id')
                image = Image.query.get(image_id)
                if image:
                    image.delete()
                    return jsonify({'message': 'Image deleted successfully'})
                else:
                    return {'message': 'Image not found'}, 404
            except Exception as e:
                return {'message': str(e)}, 500

        def post(self):
            try:
                if 'file' not in request.files:
                    return {'message': 'No file part'}, 400
                file = request.files['file']
                if file.filename == '':
                    return {'message': 'No selected file'}, 400
                filename = file.filename
                mimetype = file.mimetype
                image_data = file.read()
                upload_date = datetime.now()
                image = Image(filename=filename, mimetype=mimetype, image_data=image_data, upload_date=upload_date)
                image.create()
                return {'sucess': True}, 200
            except Exception as e:
                return {'message': str(e)}, 500

        def get(self):
            try:
                images = Image.query.all()
                imgID = random.randint(0,len(images))
                # Assuming each image has a 'image_data' attribute which stores the image data
                image_data = images[imgID].image_data  # Assuming you are only returning one image for simplicity
                return send_file(io.BytesIO(image_data), mimetype='image/png')  # Adjust mimetype as needed
            except Exception as e:
                return {'message': str(e)}, 500


    api.add_resource(_CRUD, '/')