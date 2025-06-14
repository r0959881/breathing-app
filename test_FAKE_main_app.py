import requests

PET_ID = 1
url = f"http://localhost:8000/plot/{PET_ID}"

response = requests.get(url)

if response.status_code == 200:
    with open(f"plot_pet{PET_ID}.png", "wb") as f:
        f.write(response.content)
    print(f"Plot saved as plot_pet{PET_ID}.png")
else:
    print("Failed to get plot:", response.status_code, response.text)
