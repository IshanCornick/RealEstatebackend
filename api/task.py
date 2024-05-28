from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api, Resource
from __init__ import app, db, cors
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model.tasks import Task
# from auth_middleware import token_required


task_api = Blueprint('task_api', __name__, url_prefix='/api/task')  #Here, we declare the API endpoint

api = Api(task_api)

class TaskAPI:        
    class _CRUD(Resource):  
        
        def post(self): # Create method
            body = request.get_json() #Read data from the json body 

            
            #  this is basically validating the name
            taskname = body.get('taskname')
            priority = body.get('priority')
            comments = body.get('comments')
            datecreated = body.get('datecreated')
            order = body.get('order', 0)  #Order default to 0, on the front end it appears as the first thing in the table
        
            # Create Task object
            task = Task(
                taskname=taskname,
                priority=priority,
                comments=comments,
                datecreated=datecreated,
                order=order  
            )

            # Add task to database
            task = task.create()
            # if successful, returns JSON of task
            if task:
                return jsonify(task.read())

            # if this fails, program returns error message
            return {'message': f'Error processing request'}, 400

        def get(self): 
            tasks = Task.query.all()    # Read/extract all tasks from database
            json_ready = [task.read() for task in tasks]  # Prepare output in JSON
            return jsonify(json_ready) # jsonify creates Flask response object, more specific to APIs than json.dump 
        
    @task_api.route('/<int:task_id>', methods=['DELETE'])  #delete task, so method = delete
    def delete_task(task_id):
        try:
            task = Task.query.get(task_id)  # Retrieve task by ID
            if not task:
                return jsonify({'message': 'Task not found'}), 404
            db.session.delete(task)  # Delete the task
            db.session.commit()    #commit the change to the db
            return jsonify({'message': 'Task deleted successfully'}), 200
        except Exception as e:
            print(e)
            return jsonify({'message': 'Failed to delete task'}), 500

    @task_api.route('/update-order', methods=['POST'])   #updates order, so method is post to post the new order
    def update_task_order():
        new_order = request.json.get('NewOrder')  #requests new order so that it can reflect changes in the database
        if new_order:
            Task.update_task_order(new_order)
            return jsonify({'message': 'Task order updated successfully'}), 200
        else:
            return jsonify({'error': 'New order not provided'}), 400

    # Building REST API endpoint
    api.add_resource(_CRUD, '/')
