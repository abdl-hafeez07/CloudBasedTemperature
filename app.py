from flask import Flask, render_template, send_file, request, jsonify
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import pandas as pd
import io

# ==========================================
# Flask Application
# ==========================================

app = Flask(__name__)

# ==========================================
# Connect to Supabase
# ==========================================

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# Dashboard
# ==========================================

@app.route("/")
def home():

    response = (
        supabase.table("temperature_data")
        .select("*")
        .order("created_at", desc=True)
        .limit(20)
        .execute()
    )

    records = list(reversed(response.data))

    labels = []
    temperatures = []

    for row in records:
        labels.append(row["created_at"][11:19])
        temperatures.append(float(row["temperature"]))

    if records:

        latest_temp = float(records[-1]["temperature"])
        total_records = len(records)

        if latest_temp < 25:
            status = "🟢 Cool"

        elif latest_temp < 33:
            status = "🟡 Normal"

        elif latest_temp < 37:
            status = "🟠 Warm"

        else:
            status = "🔴 High"

    else:

        latest_temp = 0
        total_records = 0
        status = "No Data"

    return render_template(
        "index.html",
        records=records,
        labels=labels,
        temperatures=temperatures,
        latest_temp=latest_temp,
        total_records=total_records,
        status=status
    )

# ==========================================
# Export CSV
# ==========================================

@app.route("/export")
def export_csv():

    response = (
        supabase.table("temperature_data")
        .select("*")
        .order("created_at")
        .execute()
    )

    records = response.data

    df = pd.DataFrame(records)

    output = io.BytesIO()

    df.to_csv(output, index=False)

    output.seek(0)

    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="temperature_records.csv"
    )

# ==========================================
# REST API - GET Latest Temperature
# ==========================================

@app.route("/api/temperature", methods=["GET"])
def get_temperature():

    response = (
        supabase.table("temperature_data")
        .select("*")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if response.data:

        return jsonify({
            "success": True,
            "data": response.data[0]
        })

    return jsonify({
        "success": False,
        "message": "No temperature data found"
    })

# ==========================================
# REST API - POST Temperature
# ==========================================

@app.route("/api/temperature", methods=["POST"])
def add_temperature():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "No JSON data received"
        }), 400

    if "temperature" not in data:

        return jsonify({
            "success": False,
            "message": "Temperature field is required"
        }), 400

    temperature = float(data["temperature"])

    supabase.table("temperature_data").insert({
        "temperature": temperature
    }).execute()

    return jsonify({
        "success": True,
        "message": "Temperature inserted successfully",
        "temperature": temperature
    })

# ==========================================
# REST API - GET All Temperatures
# ==========================================

@app.route("/api/temperatures", methods=["GET"])
def get_all_temperatures():

    response = (
        supabase.table("temperature_data")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return jsonify({
        "success": True,
        "count": len(response.data),
        "data": response.data
    })

# ==========================================
# REST API - DELETE Temperature
# ==========================================

@app.route("/api/temperature/<int:record_id>", methods=["DELETE"])
def delete_temperature(record_id):

    supabase.table("temperature_data").delete().eq("id", record_id).execute()

    return jsonify({
        "success": True,
        "message": f"Record {record_id} deleted successfully"
    })

# ==========================================
# Run Flask
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)