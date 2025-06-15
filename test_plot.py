from fastapi import FastAPI, Response
import mysql.connector , json
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO

app = FastAPI()

DB_CONFIG = {
    "host": "localhost",
    "database": "breath",
    "user": "root",
    "password": "",
    "port": 3306
}

@app.get("/plot/{pet_id}")
def generate_plot(pet_id: int):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT vitals_history FROM pet_vitals WHERE pet_id = %s", (pet_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        history = json.loads(result[0]) if result and result[0] else []
        if not history:
            return {"error": "No data available"}

        # Extract RPM values
        rpms = [entry["rpm"] for entry in history]
        x = list(range(1, len(rpms) + 1))

        # Plotting
        plt.figure(figsize=(10, 5))
        plt.plot(x, rpms, marker='o', linestyle='-', linewidth=1.5, label="Breathing (RPM)")
        plt.axhline(y=30, color='red', linestyle='--', linewidth=1.5, label="Too High (30 RPM)")
        plt.axhline(y=10, color='blue', linestyle='--', linewidth=1.5, label="Too Low (10 RPM)")
        plt.ylim(0, 60)
        plt.xlabel("Reading Index")
        plt.ylabel("Breathing Rate (RPM)")
        plt.title("Last 24 Hour Breathing Values")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        return Response(content=buf.read(), media_type="image/png")
    except Exception as e:
        return {"error": str(e)}
