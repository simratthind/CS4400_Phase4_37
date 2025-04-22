from flask import Flask, render_template
from routes import register_routes

app = Flask(__name__)
register_routes(app)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)