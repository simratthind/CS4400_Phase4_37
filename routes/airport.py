from flask import Blueprint, render_template, request
from db import cursor, db

airport_bp = Blueprint("airport", __name__)

@airport_bp.route("/add_airport", methods=["GET", "POST"])
def add_airport():
    error_msg = None
    form_data = request.form if request.method == "POST" else {}

    if request.method == "POST":
        try:
            airport_id = form_data.get("airport_id", "").strip()
            airport_name = form_data.get("airport_name", "").strip()
            city = form_data.get("city", "").strip()
            state = form_data.get("state", "").strip()
            country = form_data.get("country", "").strip()
            location_id = form_data.get("location_id", "").strip()

            if not all([airport_id, airport_name, city, state, country, location_id]):
                raise ValueError("All fields are required.")

            if len(airport_id) != 3 or len(country) != 3:
                raise ValueError("Airport ID and Country must be 3 characters.")

            # Call the stored procedure
            cursor.callproc("add_airport", [
                airport_id, airport_name, city, state, country, location_id
            ])
            db.commit()

            # Verify insertion
            cursor.execute("SELECT * FROM airport WHERE airportid = %s", (airport_id,))
            if cursor.fetchone():
                return render_template("index.html")  # success
            else:
                error_msg = "Airport could not be added. Check for duplicates or invalid location ID."

        except Exception as e:
            error_msg = str(e)

    return render_template("add_airport.html", error=error_msg, form=form_data)
