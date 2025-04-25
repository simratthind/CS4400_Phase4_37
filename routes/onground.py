from flask import Blueprint, render_template
from db import cursor

onground_bp = Blueprint("onground", __name__)

@onground_bp.route("/flights_in_the_air")
def flights_on_the_ground():
    cursor.execute("SELECT * FROM flights_on_the_ground")
    results = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    return render_template("flights_on_the_ground.html", headers=headers, rows=results)
