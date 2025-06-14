import mysql.connector, json, time
from datetime import datetime
import random

DB_CONFIG = {
    "host": "localhost",
    "database": "breath",
    "user": "root",  # or your MySQL username
    "password": "",
    "port": 3306
}

def update_all_pets():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT pet_id, vitals_history FROM pet_vitals")
    pets = cursor.fetchall()

    for pet_id, history in pets:
        history = json.loads(history) if history else []

        new_rpm = random.randint(8, 35)
        new_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "rpm": new_rpm
        }

        history.append(new_entry)
        history = history[-288:]

        avg_rpm = round(sum(entry["rpm"] for entry in history) / len(history), 2)

        cursor.execute("""
            UPDATE pet_vitals
            SET 
                current_rpm = %s,
                avg_rpm = %s,
                vitals_history = %s
            WHERE pet_id = %s
        """, (
            new_rpm,
            avg_rpm,
            json.dumps(history),
            pet_id
        ))

        print(f"[✓] Updated pet {pet_id} → RPM: {new_rpm} | AVG RPM: {avg_rpm:.2f}")

    conn.commit()
    cursor.close()
    conn.close()

# Loop every 5 minutes (300s)
while True:
    update_all_pets()
    time.sleep(120)
