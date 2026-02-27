import os
import requests
from dotenv import load_dotenv
from flight_data import FlightData

load_dotenv()

TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHT_OFFERS_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
CITY_SEARCH_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"


class FlightSearch:
    def __init__(self):
        self._api_key = os.getenv("AMADEUS_API_KEY")
        self._api_secret = os.getenv("AMADEUS_API_SECRET")
        self._token = self._get_new_token()

    def _get_new_token(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret,
        }

        response = requests.post(url=TOKEN_ENDPOINT, headers=headers, data=body)
        response.raise_for_status()
        return response.json()["access_token"]

    def get_destination_code(self, city_name):
        headers = {
            "Authorization": f"Bearer {self._token}"
        }

        params = {
            "keyword": city_name,
            "max": 1,
        }

        response = requests.get(url=CITY_SEARCH_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()

        data = response.json().get("data", [])

        if not data:
            return ""

        return data[0]["iataCode"]

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {
            "Authorization": f"Bearer {self._token}"
        }

        params = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "currencyCode": "GBP",
            "max": 1,
        }

        response = requests.get(
            url=FLIGHT_OFFERS_ENDPOINT,
            headers=headers,
            params=params,
        )
        response.raise_for_status()

        data = response.json().get("data", [])

        if not data:
            return None

        first_offer = data[0]

        price = float(first_offer["price"]["grandTotal"])

        outbound = first_offer["itineraries"][0]["segments"][0]
        inbound = first_offer["itineraries"][1]["segments"][0]

        origin_airport = outbound["departure"]["iataCode"]
        destination_airport = outbound["arrival"]["iataCode"]
        out_date = outbound["departure"]["at"].split("T")[0]
        return_date = inbound["departure"]["at"].split("T")[0]

        return FlightData(
            price=price,
            origin_airport=origin_airport,
            destination_airport=destination_airport,
            out_date=out_date,
            return_date=return_date,
        )