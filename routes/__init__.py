from flask import Blueprint
from .airplane import airplane_bp
from .airport import airport_bp
from .person import person_bp
from .license import license_bp
from .flight import flight_bp
from .flights_in_the_air import flights_in_the_air_bp
from .people_in_the_air import people_in_the_air_bp
from .people_on_the_ground import people_on_the_ground_bp
from .route_summary import route_summary_bp
from .alternative_airports import alternative_airports_bp
from .crew import crew_bp
from .retire import retire_bp
from .flights_on_the_ground import flights_on_the_ground_bp
from .flightlanding import flightlanding_bp


def register_routes(app):
    app.register_blueprint(airplane_bp)
    app.register_blueprint(airport_bp)
    app.register_blueprint(person_bp)
    app.register_blueprint(license_bp)
    app.register_blueprint(flight_bp)
    app.register_blueprint(people_in_the_air_bp)
    app.register_blueprint(people_on_the_ground_bp)
    app.register_blueprint(route_summary_bp)
    app.register_blueprint(alternative_airports_bp)
    app.register_blueprint(flights_in_the_air_bp)
    app.register_blueprint(crew_bp)
    app.register_blueprint(retire_bp)
    app.register_blueprint(flights_on_the_ground_bp)
    app.register_blueprint(flightlanding_bp)

