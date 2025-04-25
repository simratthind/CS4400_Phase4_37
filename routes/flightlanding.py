from flask import Blueprint, render_template, request
from db import cursor, db

flightlanding_bp = Blueprint("flightlanding", __name__)

@flightlanding_bp.route("/flight_landing", methods=["GET", "POST"])
def flight_landing():
    error_msg = None
    result_msg = None

    if request.method == "POST":
        try:
            flight_id = request.form.get("flightID", "").strip()

            if not flight_id:
                raise ValueError("Flight ID is required.")

            # Call the flight_landing procedure
            cursor.callproc("flight_landing", [flight_id])
            db.commit()

            result_msg = f"Flight '{flight_id}' has successfully landed."
        except Exception as e:
            error_msg = str(e)

    return render_template("flight_landing.html", error=error_msg, result=result_msg)
