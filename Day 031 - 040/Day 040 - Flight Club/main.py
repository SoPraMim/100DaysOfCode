# --- Imports --- #
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

# --- Objects --- #
data_manager = DataManager()
flight_search = FlightSearch()

# --- Program --- #
# --- Program --- #
data_manager.check_codes()

users = data_manager.get_users()
mails_sent = 0
for user in users:
    routes_to_search = data_manager.get_user_routes(user)
    flights_to_report = []
    for route in routes_to_search:
        search_result = flight_search.search_flights(route)
        if search_result["_results"] > 0:
            flights_to_report.append(FlightData(search_result))
    if len(flights_to_report) > 0:
        NotificationManager(flights_to_report,user)
        mails_sent += 1
        
if mails_sent == 0:
    print("No mails were sent.")
else:
    print(f"{mails_sent} mails were sent.")
        
        