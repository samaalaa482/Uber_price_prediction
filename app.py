from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("Uber_price_model.pkl")


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Prediction
@app.route("/predict", methods=["POST"])
def predict():

    # Get values from HTML form
    pickup_longitude = float(request.form["pickup_longitude"])
    dropoff_longitude = float(request.form["dropoff_longitude"])
    dropoff_latitude = float(request.form["dropoff_latitude"])
    year = int(request.form["year"])
    distance = float(request.form["distance"])

        # Validation
    if distance <= 0:
        return render_template(
            "index.html",
            prediction_text="Distance must be greater than zero."
        )

    if year < 2000 or year > 2035:
        return render_template(
            "index.html",
            prediction_text="Please enter a valid year."
        )


    # Create DataFrame
    input_data = pd.DataFrame({
        "pickup_longitude": [pickup_longitude],
        "dropoff_longitude": [dropoff_longitude],
        "dropoff_latitude": [dropoff_latitude],
        "year": [year],
        "distance": [distance]
    })

    # Prediction
    prediction = model.predict(input_data)

    # Return result
    return render_template(
        "index.html",
        prediction_text=f"Predicted Fare: ${prediction[0]:.2f}"
    )


if __name__ == "__main__":
    app.run(debug=True)