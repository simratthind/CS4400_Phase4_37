from flask import Blueprint, render_template
from db import cursor

alternative_airports_bp = Blueprint("alternative_airports", __name__)

@alternative_airports_bp.route("/alternative_airports", methods=["GET"])
def alternative_airports():
    try:
        cursor.execute("SELECT * FROM alternative_airports")
        rows = cursor.fetchall()
        if rows:
            headers = [desc[0] for desc in cursor.description]
            return render_template("alternative_airports.html", headers=headers, rows=rows)
        else:
            return render_template("alternative_airports.html", message="No alternative airports available.")
    except Exception as e:
        return render_template("index.html", error=str(e))