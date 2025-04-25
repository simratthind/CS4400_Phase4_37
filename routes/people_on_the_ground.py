from flask import Blueprint, render_template
from db import cursor

people_on_the_ground_bp = Blueprint("people_on_the_ground", __name__)

@people_on_the_ground_bp.route("/people_on_the_ground", methods=["GET"])
def people_on_the_ground():
    try:
        cursor.execute("SELECT * FROM people_on_the_ground")
        rows = cursor.fetchall()
        if rows:
            headers = [desc[0] for desc in cursor.description]
            return render_template("people_on_the_ground.html", headers=headers, rows=rows)
        else:
            return render_template("people_on_the_ground.html", message="No people currently on the ground.")
    except Exception as e:
        return render_template("index.html", error=str(e))
