# Flight-Deals-Finder
A Python project that uses the Sheety and Amadeus APIs to manage destination data, fill in city IATA codes, and search for low-cost flights based on prices stored in a Google Sheet.

## Features

Reads destination data from a Google Sheet using Sheety
Updates missing city IATA codes automatically using the Amadeus API
Searches for flight offers between a chosen origin city and saved destinations
Compares live flight prices against the lowest prices stored in the sheet
Prints a low-price alert when a cheaper flight is found

## Technologies Used

Python
Requests
Sheety API
Amadeus API
python-dotenv

## Project Status

This project is currently functional for:

Reading and updating Google Sheet data
Retrieving city IATA codes
Searching flight prices
The notification feature (e.g. Twilio SMS alerts) has not been added in this version.

## Environment Variables

This project uses a .env file to store API credentials securely.

Required variables include:
SHEETY_ENDPOINT
SHEETY_USERNAME
SHEETY_PASSWORD
AMADEUS_API_KEY
AMADEUS_API_SECRET

# How to Run

Clone the repository

Install the required packages:

requests
python-dotenv
Create a .env file and add your API credentials
```
Run main.py
```

## Notes

The Google Sheet stores destination cities, IATA codes, and target lowest prices.
If an IATA code is missing, the program fetches it and updates the sheet.
The program then searches for flights and checks whether the current price is lower than the saved threshold.