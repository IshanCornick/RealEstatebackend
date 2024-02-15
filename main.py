import threading
from flask import Flask, render_template, request
from flask_cors import CORS  # Import CORS
from flask.cli import AppGroup

# Assuming your __init__.py initializes the Flask app and other components
from __init__ import app, db  # Removed cors import since we'll use flask_cors directly

CORS(app)  # Enable CORS for the entire app

# Your existing imports for blueprints and models
from api.user import user_api
from api.player import player_api
from projects.projects import app_projects
from model.users import initUsers
from model.players import initPlayers

db.init_app(app)

# Register blueprints and error handlers
app.register_blueprint(user_api)
app.register_blueprint(player_api)
app.register_blueprint(app_projects)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/table/')
def table():
    return render_template("table.html")

# Custom CLI commands for database initialization
custom_cli = AppGroup('custom', help='Custom commands')

@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initPlayers()

app.cli.add_command(custom_cli)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8086")
