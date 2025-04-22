from flask import Blueprint, render_template, request
from db import cursor, db

flight_bp = Blueprint("flight", __name__)

@flight_bp.route("/offer_flight", methods=["GET", "POST"])
def offer_flight():
    error_msg = None
    form_data = request.form if request.method == "POST" else {}

    if request.method == "POST":
        try:
            flight_id = form_data.get("flight_id", "").strip()
            route_id = form_data.get("route_id", "").strip()
            support_airline = form_data.get("support_airline", "").strip()
            support_tail = form_data.get("support_tail", "").strip()
            progress = form_data.get("progress", "").strip()
            next_time = form_data.get("next_time", "").strip()
            cost = form_data.get("cost", "").strip()

            if not (flight_id and route_id and progress and next_time and cost):
                raise ValueError("All required fields must be filled.")

            if not progress.isdigit() or int(progress) < 0:
                raise ValueError("Progress must be a non-negative integer.")
            if not cost.isdigit() or int(cost) < 0:
                raise ValueError("Cost must be a non-negative integer.")

            cursor.callproc("offer_flight", [
                flight_id, route_id,
                support_airline if support_airline else None,
                support_tail if support_tail else None,
                int(progress), next_time, int(cost)
            ])
            db.commit()

            cursor.execute("SELECT * FROM flight WHERE flightid = %s", (flight_id,))
            if cursor.fetchone():
                return render_template("index.html")  # success
            else:
                error_msg = "Flight could not be added. It may already exist or violate constraints."

        except Exception as e:
            error_msg = str(e)

    return render_template("offer_flight.html", error=error_msg, form=form_data)
