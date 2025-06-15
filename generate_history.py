import json
from datetime import datetime, timedelta
import random

choice = input("Type 'dog' for normal data or 'cat' for spiky data: ").strip().lower()
now = datetime.utcnow()

if choice == "dog":
    dog_history = [
        {"timestamp": (now - timedelta(minutes=2*i)).isoformat() + "Z", "rpm": 18 + (i % 3)}
        for i in range(30)
    ]
    print(json.dumps(dog_history))
elif choice == "cat":
    cat_history = [
        {"timestamp": (now - timedelta(minutes=2*i)).isoformat() + "Z", "rpm": random.choice([12, 13, 14, 35, 36, 37])}
        for i in range(30)
    ]
    print(json.dumps(cat_history))
else:
    print("Invalid choice. Please type 'dog' or 'cat'.")