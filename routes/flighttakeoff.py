from flask import Blueprint, render_template, request
from db import cursor, db

flighttakeoff_bp = Blueprint("flighttakeoff", __name__)

@flighttakeoff_bp.route("/flight_takeoff", methods=["GET", "POST"])
def flight_takeoff():
    error_msg = None
    success_msg = None
    form_data = request.form if request.method == "POST" else {}

    if request.method == "POST":
        try:
            flight_id = form_data.get("flightID", "").strip()

            if not flight_id:
                raise ValueError("Flight ID is required.")

            # Check if the flight exists and get its current state
            cursor.execute("""
                SELECT airplane_status, progress, routeID, support_tail
                FROM flight
                WHERE flightID = %s
            """, (flight_id,))
            flight = cursor.fetchone()
            if not flight:
                raise ValueError("Flight ID does not exist.")

            status, progress, route_id, support_tail = flight

            # Check if the flight is already in flight
            if status == 'in_flight':
                raise ValueError("Flight is already in the air.")

            # Check if the flight has reached the end of its route
            cursor.execute("""
                SELECT MAX(sequence)
                FROM route_path
                WHERE routeID = %s
            """, (route_id,))
            max_sequence = cursor.fetchone()[0]
            if progress >= max_sequence:
                raise ValueError("Flight has reached its final destination.")

            # Check pilot requirements
            cursor.execute("""
                SELECT plane_type
                FROM airplane
                WHERE tail_num = %s
            """, (support_tail,))
            plane_type = cursor.fetchone()[0] if support_tail else None

            if plane_type:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM pilot
                    WHERE commanding_flight = %s
                """, (flight_id,))
                pilot_count = cursor.fetchone()[0]

                if (plane_type in ['Airbus', 'General'] and pilot_count < 1) or \
                   (plane_type == 'Boeing' and pilot_count < 2):
                    # Simulate the procedure's behavior: delay by 30 minutes
                    cursor.execute("""
                        UPDATE flight
                        SET next_time = ADDTIME(next_time, '00:30:00')
                        WHERE flightID = %s
                    """, (flight_id,))
                    db.commit()
                    raise ValueError(f"Not enough pilots for {plane_type} plane. Flight delayed by 30 minutes.")

            # Call the stored procedure
            cursor.callproc("flight_takeoff", [flight_id])
            db.commit()

            # Verify the flight status after the procedure
            cursor.execute("""
                SELECT airplane_status, next_time
                FROM flight
                WHERE flightID = %s
            """, (flight_id,))
            new_status = cursor.fetchone()
            if new_status and new_status[0] == 'in_flight':
                success_msg = f"Flight '{flight_id}' has successfully taken off."
                return render_template("index.html", success_msg=success_msg)
            else:
                error_msg = "Flight could not take off. Please check flight status or pilot assignments."

        except Exception as e:
            error_msg = str(e)

    return render_template("flight_takeoff.html", error=error_msg, form=form_data)