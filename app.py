from flask import Flask, render_template
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# Flask App
app = Flask(__name__)

# Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


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

    # Reverse so oldest appears first in table and graph
    records = list(reversed(response.data))

    labels = []
    temperatures = []

    for row in records:
        labels.append(row["created_at"][11:19])      # HH:MM:SS
        temperatures.append(float(row["temperature"]))

    # Dashboard Cards
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


if __name__ == "__main__":
    app.run(debug=True)