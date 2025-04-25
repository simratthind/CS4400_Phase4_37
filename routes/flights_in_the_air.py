from flask import Blueprint, render_template
from db import cursor

flights_in_the_air_bp = Blueprint("flights_in_the_air", __name__)

@flights_in_the_air_bp.route("/flights_in_the_air")
def flights_in_the_air():
    cursor.execute("SELECT * FROM flights_in_the_air")
    results = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    return render_template("flights_in_the_air.html", headers=headers, rows=results)
