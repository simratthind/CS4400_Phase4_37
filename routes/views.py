from flask import Blueprint, render_template
from db import cursorgitp 

views_bp = Blueprint("views", __name__)

@views_bp.route("/flights_in_the_air")
def flights_in_the_air():
    cursor.execute("SELECT * FROM flights_in_the_air")
    results = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    return render_template("flights_in_the_air.html", headers=headers, rows=results)
