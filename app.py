from flask import Flask, render_template, send_file
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import pandas as pd
import io

# -----------------------------------------
# Flask Application
# -----------------------------------------

app = Flask(__name__)

# -----------------------------------------
# Connect to Supabase
# -----------------------------------------

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# -----------------------------------------
# Home Page
# -----------------------------------------

@app.route("/")
def home():

    # Fetch latest 20 records
    response = (
        supabase.table("temperature_data")
        .select("*")
        .order("created_at", desc=True)
        .limit(20)
        .execute()
    )

    # Display oldest to newest
    records = list(reversed(response.data))

    labels = []
    temperatures = []

    for row in records:
        labels.append(row["created_at"][11:19])      # HH:MM:SS
        temperatures.append(float(row["temperature"]))

    # Dashboard Information

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


# -----------------------------------------
# Export CSV
# -----------------------------------------

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


# -----------------------------------------
# Run Flask
# -----------------------------------------

if __name__ == "__main__":
    app.run(debug=True)