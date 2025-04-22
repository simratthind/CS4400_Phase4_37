from flask import Blueprint, render_template, request
from db import cursor, db

person_bp = Blueprint("person", __name__)

@person_bp.route("/add_person", methods=["GET", "POST"])
def add_person():
    error_msg = None
    form_data = request.form if request.method == "POST" else {}

    if request.method == "POST":
        try:
            person_id = form_data.get("person_id", "").strip()
            first_name = form_data.get("first_name", "").strip()
            last_name = form_data.get("last_name", "").strip()
            location_id = form_data.get("location_id", "").strip()
            tax_id = form_data.get("tax_id", "").strip()
            experience = form_data.get("experience", "").strip()
            miles = form_data.get("miles", "").strip()
            funds = form_data.get("funds", "").strip()

            if not person_id or not first_name or not location_id:
                raise ValueError("Person ID, First Name, and Location ID are required.")

            if tax_id and (experience == "" or not experience.isdigit()):
                raise ValueError("Pilots must have a valid experience value.")
            if miles and not miles.isdigit():
                raise ValueError("Miles must be a number.")
            if funds and not funds.isdigit():
                raise ValueError("Funds must be a number.")

            # If tax_id + experience = pilot, else = passenger
            cursor.callproc("add_person", [
                person_id, first_name, last_name, location_id,
                tax_id if tax_id else None,
                int(experience) if experience else None,
                int(miles) if miles else None,
                int(funds) if funds else None
            ])
            db.commit()

            # Confirm insert happened
            cursor.execute("SELECT * FROM person WHERE personid = %s", (person_id,))
            if cursor.fetchone():
                return render_template("index.html")  # Success
            else:
                error_msg = "Person could not be added. Check constraints."
        except Exception as e:
            error_msg = str(e)

    return render_template("add_person.html", error=error_msg, form=form_data)
