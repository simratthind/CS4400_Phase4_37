from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL connection setup
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="devik2005",
        database="flight_tracking"
    )
    return connection

@app.route('/')
def index():
    return render_template('index.html')  # Assuming index.html is your homepage.

@app.route('/flight_landing', methods=['GET', 'POST'])
def flight_landing():
    result = None
    error = None

    if request.method == 'POST':
        flight_id = request.form['flightID']

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Call the stored procedure `flight_landing` with the flight ID
            cursor.callproc('flight_landing', [flight_id])

            # Commit the transaction to apply changes
            conn.commit()

            # Success message
            result = f"Procedure executed successfully for Flight ID: {flight_id}"
        except mysql.connector.Error as err:
            # Error handling
            error = f"Error: {err}"
        finally:
            # Close the database connection
            cursor.close()
            conn.close()

    return render_template('flight_landing_form.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)