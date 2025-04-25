from flask import Blueprint, render_template, request
from db import cursor, db

passengersboard_bp = Blueprint("passengersboard", __name__)

@passengersboard_bp.route("/pass_board", methods=["GET", "POST"])
def passengersboard():
    error_msg = None
    data = {
        "airline_id": "",
        "tail_num": "",
        "seat_cap": "",
        "speed": "",
        "location_id": "",
        "plane_type": "",
        "maintained": "",
        "model": "",
        "neo": ""
    }
    form_data = request.form if request.method == "POST" else {}

    if request.method == "POST":
        try:
            airline_id = form_data.get("airline_id", "").strip()
            tail_num = form_data.get("tail_num", "").strip()
            seat_cap = form_data.get("seat_cap", "").strip()
            speed = form_data.get("speed", "").strip()
            location_id = form_data.get("location_id", "").strip()
            plane_type = form_data.get("plane_type", "").strip()
            maintained = form_data.get("maintained", "").strip().lower() == "true"
            model = form_data.get("model", "").strip()
            neo = form_data.get("neo", "").strip()

            if not (airline_id and tail_num and seat_cap and speed and location_id and plane_type):
                raise ValueError("All required fields must be filled.")

            if not seat_cap.isdigit() or int(seat_cap) <= 0:
                raise ValueError("Seat capacity must be a positive number.")
            if not speed.isdigit() or int(speed) <= 0:
                raise ValueError("Speed must be a positive number.")

            if plane_type not in ["Airbus", "Boeing", "General"]:
                raise ValueError("Plane type must be Boeing, Airbus, or General.")

            if plane_type == "Airbus" and neo not in ["0", "1"]:
                raise ValueError("Airbus planes must specify neo (0 or 1).")
            if plane_type == "General" and (model or neo):
                raise ValueError("General planes cannot have a model or neo value.")

            cursor.callproc("add_airplane", [
                airline_id, tail_num, int(seat_cap), int(speed),
                location_id, plane_type, maintained,
                model if model else None,
                int(neo) if neo else None
            ])
            db.commit()

            # Check if airplane was actually inserted
            cursor.execute("SELECT * FROM airplane WHERE airlineid = %s AND tail_num = %s", (airline_id, tail_num))
            if cursor.fetchone():
                return render_template("index.html", success_msg="Airplane successfully added!")
            else:
                error_msg = "Airplane could not be added. It may already exist or violate constraints."
        except Exception as e:
            error_msg = str(e)

    return render_template("pass_board.html", error=error_msg, form=form_data)
