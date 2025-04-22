from flask import Blueprint
from .airplane import airplane_bp
from .airport import airport_bp
from .person import person_bp
from .license import license_bp
from .flight import flight_bp

def register_routes(app):
    app.register_blueprint(airplane_bp)
    app.register_blueprint(airport_bp)
    app.register_blueprint(person_bp)
    app.register_blueprint(license_bp)
    app.register_blueprint(flight_bp)

