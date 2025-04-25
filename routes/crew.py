from flask import Blueprint, render_template, request
from db import cursor, db

crew_bp = Blueprint("crew", __name__)

@crew_bp.route("/recycle_crew", methods=["GET", "POST"])
def recycle_crew():
    error_msg = None
    form_data = request.form if request.method == "POST" else {}

    if request.method == "POST":
        try:
            flight_id = form_data.get("flight_id", "").strip()

            if not (flight_id):
                raise ValueError("All required fields must be filled.")

            cursor.callproc("recycle_crew", [
                flight_id])
            db.commit()

            # Check if airplane was actually inserted
            cursor.execute("SELECT * FROM flight WHERE flightid = %s")
            if cursor.fetchone():
                return render_template("index.html", success_msg="Successful crew recycled!")
            else:
                error_msg = "Crew could not be recycled. It may already exist or violate constraints."
        except Exception as e:
            error_msg = str(e)

    return render_template("recycle_crew.html", error=error_msg, form=form_data)
