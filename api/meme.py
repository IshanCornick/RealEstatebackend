from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource
from datetime import datetime
from auth_middleware import token_required
from model.memes import Image  # Assuming Image is the SQLAlchemy model for storing images

user_api = Blueprint('user_api', __name__, url_prefix='/api/users')
api = Api(user_api)

class ImageAPI:        
    class _CRUD(Resource):
        @token_required
        def put(self, current_user):
            body = request.get_json()
            image_id = body.get('id')
            filename = body.get('filename')
            mimetype = body.get('mimetype')
            image_data = body.get('image_data')
            # Assuming you have a method like update() in your Image model
            image = Image.query.filter_by(id=image_id).first()
            if image:
                image.update(filename, mimetype, image_data)
                return jsonify(image.read())
            else:
                return {'message': 'Image not found'}, 404

        @token_required
        def delete(self, current_user):
            image_id = request.args.get('id')
            image = Image.query.get(image_id)
            if image:
                image.delete()
                return jsonify({'message': 'Image deleted successfully'})
            else:
                return {'message': 'Image not found'}, 404

        def post(self):
            filename = request.files['file'].filename
            mimetype = request.files['file'].mimetype
            image_data = request.files['file'].read()
            upload_date = datetime.now()
            image = Image(filename=filename, mimetype=mimetype, image_data=image_data, upload_date=upload_date)
            image.create()
            return jsonify(image.read())

        @token_required
        def get(self, current_user):
            images = Image.query.all()
            json_ready = [image.read() for image in images]
            return jsonify(json_ready)

    api.add_resource(_CRUD, '/')
