from flask import Blueprint, render_template, request
from db import cursor, db

license_bp = Blueprint("license", __name__)

@license_bp.route("/toggle_license", methods=["GET", "POST"])
def toggle_license():
    error_msg = None
    form_data = request.form if request.method == "POST" else {}

    if request.method == "POST":
        try:
            person_id = form_data.get("person_id", "").strip()
            license_type = form_data.get("license", "").strip()

            if not person_id or not license_type:
                raise ValueError("Both Pilot ID and License Type are required.")

            # Call the stored procedure
            cursor.callproc("grant_or_revoke_pilot_license", [person_id, license_type])
            db.commit()

            # Check result (optional: see if pilot now has license or not)
            return render_template("index.html")
        except Exception as e:
            error_msg = str(e)

    return render_template("toggle_license.html", error=error_msg, form=form_data)
