# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve
# the program requirements.

import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

load_dotenv()

# create the Data Manager:
data_manager = DataManager(os.getenv('SHEETY_ENDPOINT'), os.getenv('SHEETY_BEARER_TOKEN'))

# Get data from Google Sheets using the Sheety API:
flight_data = data_manager.get_flight_data()
users = data_manager.get_users()

# TEST DATA
# flight_data = [
#     {'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 85, 'id': 2},
#     {'city': 'Berlin', 'iataCode': 'BER', 'lowestPrice': 70, 'id': 3},
#     {'city': 'Tokyo', 'iataCode': 'TYO', 'lowestPrice': 520, 'id': 4},
#     {'city': 'Sydney', 'iataCode': 'SYD', 'lowestPrice': 1050, 'id': 5},
#     {'city': 'Istanbul', 'iataCode': 'IST', 'lowestPrice': 110, 'id': 6},
#     {'city': 'Kuala Lumpur', 'iataCode': 'KUL', 'lowestPrice': 520, 'id': 7},
#     {'city': 'New York', 'iataCode': 'NYC', 'lowestPrice': 500, 'id': 8},
#     {'city': 'San Francisco', 'iataCode': 'SFO', 'lowestPrice': 600, 'id': 9},
#     {'city': 'Cape Town', 'iataCode': 'CPT', 'lowestPrice': 450, 'id': 10},
#     {'city': 'Bali', 'iataCode': 'DPS', 'lowestPrice': 700, 'id': 11},
#     {'city': 'Nairobi', 'iataCode': 'NBO', 'lowestPrice': 430, 'id': 12}
# ]
# users = [
#     {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'example@test.com', 'id': 2},
# ]


flight_search = FlightSearch(os.getenv('TEQUILA_ENDPOINT'), os.getenv('TEQUILA_API_KEY'))
notification_manager = NotificationManager(
    from_email=os.getenv('FROM_EMAIL'),
    password=os.getenv('EMAIL_PASSWORD'),
    smtp=os.getenv('SMTP')
)

for entry in flight_data:
    # Add missing IATA codes for destinations
    if entry['iataCode'] == '':
        entry['iataCode'] = flight_search.get_iata_code({"term": f"{entry['city']}"})
        data_manager.update_flight_data(entry['id'], entry)

    # Search flights for each destination
    flight = flight_search.search_flights(
        destination=entry['iataCode'],
        date_from=datetime.now(),
        date_to=datetime.now() + timedelta(weeks=26),
        max_stops=0
    )

    # Email every user for each flight that has a price <= lowest price
    if flight and flight.price <= entry['lowestPrice']:
        google_flight_link = f"https://www.google.co.uk/flights/?hl=en#flt={flight.departure_airport_code}." \
                             f"{flight.destination_airport_code}.{flight.outbound_date}*" \
                             f"{flight.destination_airport_code}.{flight.departure_airport_code}.{flight.return_date}"

        email_msg = f"Subject: Low price alert! \n\n" \
                    f"Low price alert! " \
                    f"Only {flight.price} Euro to fly from " \
                    f"{flight.departure_city}-{flight.departure_airport_code} to " \
                    f"{flight.destination}-{flight.destination_airport_code}, from " \
                    f"{flight.outbound_date} to {flight.return_date}. \n"

        if flight.stop_overs == 0:
            email_msg += "Direct flight. \n"
        elif flight.stop_overs == 1 or flight.via_cities[0] == flight.via_cities[1]:
            email_msg += f"Flight with 1 stop over, via {flight.via_cities[0]}. \n"
        else:
            email_msg += f"Flight with 1 stop over, outbound flight via {flight.via_cities[0]} " \
                         f"and return flight via {flight.via_cities[1]}. \n"

        email_msg += f"{google_flight_link}"
        print(email_msg)
        for user in users:
            notification_manager.send_email(message=email_msg, to_email=user['email'])
