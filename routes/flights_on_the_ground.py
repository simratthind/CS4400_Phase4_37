from flask import Blueprint, render_template
from db import cursor

flights_on_the_ground_bp = Blueprint("flights_on_the_ground", __name__)

@flights_on_the_ground_bp.route("/flights_on_the_ground")
def flights_on_the_ground():
    cursor.execute("SELECT * FROM flights_on_the_ground")
    results = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    return render_template("flights_on_the_ground.html", headers=headers, rows=results)
