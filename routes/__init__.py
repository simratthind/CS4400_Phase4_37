from flask import Blueprint
from .airplane import airplane_bp
from .airport import airport_bp
from .person import person_bp
from .license import license_bp
from .flight import flight_bp
from .views import views_bp
from .crew import crew_bp
from .retire import retire_bp
from .onground import onground_bp


def register_routes(app):
    app.register_blueprint(airplane_bp)
    app.register_blueprint(airport_bp)
    app.register_blueprint(person_bp)
    app.register_blueprint(license_bp)
    app.register_blueprint(flight_bp)
    app.register_blueprint(views_bp)
    app.register_blueprint(crew_bp)
    app.register_blueprint(retire_bp)
    app.register_blueprint(onground_bp)


