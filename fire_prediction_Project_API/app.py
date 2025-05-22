
from flask import Flask
from fire_predictor.routes import fire_predictor_bp
from live_data.routes import live_data_bp
from joblib import load

app = Flask(__name__)



app.register_blueprint(fire_predictor_bp)
app.register_blueprint(live_data_bp)

@app.route("/")
def home():
    return "Up and Running"

if __name__ == "__main__":
    app.run(debug=True)