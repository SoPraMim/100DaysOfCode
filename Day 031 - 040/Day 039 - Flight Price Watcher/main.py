# --- Imports --- #
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

# --- Objects --- #
data_manager = DataManager()
flight_search = FlightSearch()

# --- Program --- #
flights_data = data_manager.get_flight_data()
flights_to_report = []
for flight in flights_data:
    search_result = flight_search.search_flights(flight)
    if search_result["_results"] > 0:
        flights_to_report.append(FlightData(search_result))
        
if len(flights_to_report) > 0:
    NotificationManager(flights_to_report)
    print("Mail sent!")