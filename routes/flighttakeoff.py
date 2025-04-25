from flask import Blueprint, render_template, request
from db import cursor, db

flighttakeoff_bp = Blueprint("flighttakeoff", __name__)

@flighttakeoff_bp.route("/flight_takeoff", methods=["GET", "POST"])
def flight_takeoff():
    error_msg = None
    result_msg = None

    if request.method == "POST":
        try:
            flight_id = request.form.get("flightID", "").strip()

            if not flight_id:
                raise ValueError("Flight ID is required.")

            # Call the stored procedure
            cursor.callproc("flight_takeoff", [flight_id])
            db.commit()

            result_msg = f"Flight '{flight_id}' has successfully taken off."
        except Exception as e:
            error_msg = str(e)

    return render_template("flight_takeoff.html", error=error_msg, result=result_msg)
