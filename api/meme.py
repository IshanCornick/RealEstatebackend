from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource
from datetime import datetime
from auth_middleware import token_required
from model.memes import Image  # Assuming Image is the SQLAlchemy model for storing images

meme_api = Blueprint('meme_api', __name__, 
                     url_prefix='/api/memes')

api = Api(meme_api)

class ImageAPI:        
    class _CRUD(Resource):
        @token_required
        def put(self, current_user):
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

        @token_required
        def delete(self, current_user):
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
                return jsonify(image.read())
            except Exception as e:
                return {'message': str(e)}, 500

        @token_required
        def get(self, current_user):
            try:
                images = Image.query.all()
                json_ready = [image.read() for image in images]
                return jsonify(json_ready)
            except Exception as e:
                return {'message': str(e)}, 500

    api.add_resource(_CRUD, '/')