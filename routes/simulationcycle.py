from flask import Blueprint, render_template, request
from db import cursor, db

simulationcycle_bp = Blueprint("simulationcycle", __name__)

@simulationcycle_bp.route("/simulation_cycle", methods=["GET", "POST"])
def simulation_cycle():
    sim_success = None
    error_msg = None
    form_data = request.form if request.method == "POST" else {}

    if request.method == "POST":
        try:
            cursor.callproc("simulation_cycle")
            db.commit()
            sim_success = "Simulation cycle executed successfully."
        except Exception as e:
            error_msg = str(e)

    return render_template("simulation_cycle.html", error=error_msg, sim_success=sim_success)
