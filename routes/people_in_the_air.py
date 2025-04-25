from flask import Blueprint, render_template
from db import cursor

people_in_the_air_bp = Blueprint("people_in_the_air", __name__)

@people_in_the_air_bp.route("/people_in_the_air", methods=["GET"])
def people_in_the_air():
    try:
        cursor.execute("SELECT * FROM people_in_the_air")
        rows = cursor.fetchall()
        if rows:
            headers = [desc[0] for desc in cursor.description]
            return render_template("people_in_the_air.html", headers=headers, rows=rows)
        else:
            return render_template("people_in_the_air.html", message="No people currently in the air.")
    except Exception as e:
        return render_template("index.html", error=str(e))