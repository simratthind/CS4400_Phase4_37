from flask import Blueprint, render_template
from db import cursor

route_summary_bp = Blueprint("route_summary", __name__)

@route_summary_bp.route("/route_summary", methods=["GET"])
def route_summary():
    try:
        cursor.execute("SELECT * FROM route_summary")
        rows = cursor.fetchall()
        if rows:
            headers = [desc[0] for desc in cursor.description]
            return render_template("route_summary.html", headers=headers, rows=rows)
        else:
            return render_template("route_summary.html", message="No route summary available.")
    except Exception as e:
        return render_template("index.html", error=str(e))