from datetime import datetime, timedelta
from data_manager import DataManager
from dotenv import load_dotenv
from flight_search import FlightSearch
import requests
import os

load_dotenv()

username = os.getenv("SHEETY_USERNAME")
password = os.getenv("SHEETY_PASSWORD")
endpoint = os.getenv("SHEETY_ENDPOINT")

flight_search = FlightSearch()
data_manager = DataManager(endpoint, username, password)
sheet_data = data_manager.prices

# Step 1: fill any missing IATA codes
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])

        update_id = row["id"]
        put_url = f"{endpoint}/{update_id}"

        payload = {
            "price": {
                "iataCode": row["iataCode"],
            }
        }

        response = requests.put(put_url, json=payload, auth=(username, password))
        response.raise_for_status()

# Step 2: search flights and compare prices
tomorrow = datetime.now() + timedelta(days=1)
six_months_from_now = datetime.now() + timedelta(days=180)

for row in sheet_data:
    flight = flight_search.check_flights(
        origin_city_code="LON",   # change this if your departure city is different
        destination_city_code=row["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_now,
    )

    if flight is None:
        print(f"No flights found for {row['city']}.")
        continue

    if flight.price < row["lowestPrice"]:
        print(
            f"Low price alert! Only £{flight.price} to fly from "
            f"{flight.origin_airport} to {flight.destination_airport}, "
            f"from {flight.out_date} to {flight.return_date}."
        )