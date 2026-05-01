# from flask import Flask, request, jsonify
# import joblib
# import pandas as pd
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Load model
# model = joblib.load("crop_price_model.pkl")

# # Load dataset
# df = pd.read_csv("AgroTrade_Maharashtra_Crop_Prices_With_Profit.csv")
# df.columns = df.columns.str.strip()


# @app.route("/")
# def home():
#     return "Backend Running ✅"


# # ===============================
# # 🔹 PROFIT + PREDICTION (FIXED)
# # ===============================
# @app.route("/predict", methods=["POST"])
# def predict():
#     try:
#         data = request.json

#         # Handle both formats (IMPORTANT)
#         crop = data.get("crop") or data.get("Crop")
#         season = data.get("season") or data.get("Season")
#         state = data.get("state") or data.get("State")
#         market = data.get("market") or data.get("Market")
#         month = data.get("month") or data.get("Month")
#         year = data.get("year") or data.get("Year")
#         cost = data.get("cost") or data.get("Cost_per_Quintal")

#         if not all([crop, season, state, market, month, year, cost]):
#             return jsonify({"error": "Missing required fields"})

#         # Format fix
#         crop = crop.capitalize()
#         season = season.capitalize()
#         state = state.capitalize()
#         market = market.capitalize()

#         input_data = pd.DataFrame([{
#             "Month": int(month),
#             "State": state,
#             "Cost_per_Quintal": float(cost),
#             "Season": season,
#             "Crop": crop,
#             "Market": market,
#             "Year": int(year)
#         }])

#         prediction = model.predict(input_data)[0]
#         profit = float(prediction) - float(cost)

#         return jsonify({
#             "predicted_price": float(prediction),
#             "profit": float(profit)
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)})


# # ==================================
# # 🔹 SEASONAL ANALYSIS (UNCHANGED)
# # ==================================
# @app.route("/seasonal-analysis", methods=["POST"])
# def seasonal_analysis():
#     try:
#         data = request.json
#         season = data["season"].capitalize()

#         filtered = df[df["Season"] == season]

#         if filtered.empty:
#             return jsonify({"error": "No data for this season"})

#         avg_price = filtered["Price_per_Quintal"].mean()

#         sample = filtered.iloc[0:1].copy()

#         sample_input = pd.DataFrame([{
#             "Month": int(sample["Month"].values[0]),
#             "State": sample["State"].values[0],
#             "Cost_per_Quintal": float(sample["Cost_per_Quintal"].values[0]),
#             "Season": sample["Season"].values[0],
#             "Crop": sample["Crop"].values[0],
#             "Market": sample["Market"].values[0],
#             "Year": int(sample["Year"].values[0])
#         }])

#         predicted_price = model.predict(sample_input)[0]

#         overall_avg = df["Price_per_Quintal"].mean()

#         if avg_price > overall_avg:
#             insight = "Prices are generally HIGHER in this season 📈"
#         else:
#             insight = "Prices are generally LOWER in this season 📉"

#         return jsonify({
#             "average_price": float(avg_price),
#             "predicted_price": float(predicted_price),
#             "insight": insight
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)})


# # ==================================
# # 🔹 DASHBOARD API (NEW)
# # ==================================
# @app.route("/dashboard", methods=["GET"])
# def dashboard():
#     try:
#         # Average price
#         avg_price = df["Price_per_Quintal"].mean()

#         # Profit column
#         df["Profit"] = df["Price_per_Quintal"] - df["Cost_per_Quintal"]

#         # Most profitable crop
#         profitable_crop = df.groupby("Crop")["Profit"].mean().idxmax()

#         # High-risk crop (highest variation)
#         high_risk_crop = df.groupby("Crop")["Price_per_Quintal"].std().idxmax()

#         # Best season
#         best_season = df.groupby("Season")["Price_per_Quintal"].mean().idxmax()

#         # Monthly trend
#         trend = df.groupby("Month")["Price_per_Quintal"].mean().reset_index()

#         # Crop comparison
#         crop_data = df.groupby("Crop")["Price_per_Quintal"].mean().reset_index()

#         return jsonify({
#             "avg_price": float(avg_price),
#             "most_profitable_crop": profitable_crop,
#             "high_risk_crop": high_risk_crop,
#             "best_season": best_season,
#             "trend": trend.to_dict(orient="records"),
#             "crop_data": crop_data.to_dict(orient="records")
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)})


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS
import os

app = Flask(__name__)

# ✅ Restrict CORS (change after frontend deploy)
CORS(app, origins=["*"])  # later replace with your Vercel URL

# ✅ Load model safely
model = joblib.load("crop_price_model.pkl")

# ✅ Load dataset
df = pd.read_csv("AgroTrade_Maharashtra_Crop_Prices_With_Profit.csv")
df.columns = df.columns.str.strip()


@app.route("/")
def home():
    return "Backend Running ✅"


# ===============================
# 🔹 PREDICT
# ===============================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        crop = data.get("crop") or data.get("Crop")
        season = data.get("season") or data.get("Season")
        state = data.get("state") or data.get("State")
        market = data.get("market") or data.get("Market")
        month = data.get("month") or data.get("Month")
        year = data.get("year") or data.get("Year")
        cost = data.get("cost") or data.get("Cost_per_Quintal")

        if not all([crop, season, state, market, month, year, cost]):
            return jsonify({"error": "Missing required fields"})

        input_data = pd.DataFrame([{
            "Month": int(month),
            "State": crop.capitalize(),
            "Cost_per_Quintal": float(cost),
            "Season": season.capitalize(),
            "Crop": crop.capitalize(),
            "Market": market.capitalize(),
            "Year": int(year)
        }])

        prediction = model.predict(input_data)[0]
        profit = float(prediction) - float(cost)

        return jsonify({
            "predicted_price": float(prediction),
            "profit": float(profit)
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# ===============================
# 🔹 SEASONAL ANALYSIS
# ===============================
@app.route("/seasonal-analysis", methods=["POST"])
def seasonal_analysis():
    try:
        data = request.json
        season = data["season"].capitalize()

        filtered = df[df["Season"] == season]

        if filtered.empty:
            return jsonify({"error": "No data for this season"})

        avg_price = filtered["Price_per_Quintal"].mean()

        sample = filtered.iloc[0:1].copy()

        sample_input = pd.DataFrame([{
            "Month": int(sample["Month"].values[0]),
            "State": sample["State"].values[0],
            "Cost_per_Quintal": float(sample["Cost_per_Quintal"].values[0]),
            "Season": sample["Season"].values[0],
            "Crop": sample["Crop"].values[0],
            "Market": sample["Market"].values[0],
            "Year": int(sample["Year"].values[0])
        }])

        predicted_price = model.predict(sample_input)[0]
        overall_avg = df["Price_per_Quintal"].mean()

        insight = "Prices are generally HIGHER in this season 📈" if avg_price > overall_avg else "Prices are generally LOWER in this season 📉"

        return jsonify({
            "average_price": float(avg_price),
            "predicted_price": float(predicted_price),
            "insight": insight
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# ===============================
# 🔹 DASHBOARD
# ===============================
@app.route("/dashboard", methods=["GET"])
def dashboard():
    try:
        df["Profit"] = df["Price_per_Quintal"] - df["Cost_per_Quintal"]

        return jsonify({
            "avg_price": float(df["Price_per_Quintal"].mean()),
            "most_profitable_crop": df.groupby("Crop")["Profit"].mean().idxmax(),
            "high_risk_crop": df.groupby("Crop")["Price_per_Quintal"].std().idxmax(),
            "best_season": df.groupby("Season")["Price_per_Quintal"].mean().idxmax(),
            "trend": df.groupby("Month")["Price_per_Quintal"].mean().reset_index().to_dict(orient="records"),
            "crop_data": df.groupby("Crop")["Price_per_Quintal"].mean().reset_index().to_dict(orient="records")
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# ✅ IMPORTANT FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)