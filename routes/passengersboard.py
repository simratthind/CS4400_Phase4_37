from flask import Blueprint, render_template, request
from db import cursor, db

passengersboard_bp = Blueprint("passengersboard", __name__)

@passengersboard_bp.route("/pass_board", methods=["GET", "POST"])
def passengersboard():
    error_msg = None
    data = {
        "airline_id": ""
    }
    form_data = request.form if request.method == "POST" else {}

    if request.method == "POST":
        try:
            airline_id = form_data.get("airline_id", "").strip()

            if not (airline_id and tail_num and seat_cap and speed and location_id and plane_type):
                raise ValueError("All required fields must be filled.")


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
