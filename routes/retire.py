from flask import Blueprint, render_template, request
from db import cursor, db

airplane_bp = Blueprint("retire", __name__)

@airplane_bp.route("/retire_flight", methods=["GET", "POST"])
def retire_flight():
    error_msg = None
    form_data = request.form if request.method == "POST" else {}

    if request.method == "POST":
        try:
            flight_id = form_data.get("flight_id", "").strip()

            if not (flight_id):
                raise ValueError("All required fields must be filled.")

            cursor.callproc("retire_flight", [
                flight_id])
            db.commit()

            # Check if airplane was actually inserted
            cursor.execute("SELECT * FROM flight WHERE flightid = %s")
            if cursor.fetchone():
                return render_template("index.html", success_msg="Successful flight retired!")
            else:
                error_msg = "Flight could not be retired. It may already exist or violate constraints."
        except Exception as e:
            error_msg = str(e)

    return render_template("retire_flight.html", error=error_msg, form=form_data)
