import http.client
import json

conn = http.client.HTTPSConnection("developers.cathaypacific.com")

headers = {
    "accept": "application/json",
    "apiKey": "QcycZMTWabJaQUvw8dg2kZI4mlCd9Fot"
}

def get_passenger_detail(pid):
    passenger_details = ""
    conn.request("GET", f"/hackathon-apigw/airport/customers/{pid}/details", headers=headers)

    res = conn.getresponse()
    data = res.read()
    user_details = json.loads(data.decode("utf-8"))

    passenger_data = user_details["data"]

    # Extract passenger details
    passenger_id = passenger_data["id"]
    record_locator = passenger_data["recordLocator"]
    is_exact_match = passenger_data["isExactMatch"]
    is_unique_match = passenger_data["isUniqueMatch"]

    passenger_details = f"Passenger ID: {passenger_id}\n" \
                        f"Record Locator: {record_locator}\n" \
                        f"Is Exact Match: {is_exact_match}\n" \
                        f"Is Unique Match: {is_unique_match}\n\n"

    # Extract traveler details
    traveler = passenger_data["traveler"]
    traveler_name = traveler["name"]
    first_name = traveler_name["firstName"]
    last_name = traveler_name["lastName"]
    prefix = traveler_name["prefix"]
    gender = traveler["gender"]

    # Check if dateOfBirth field is present
    if "dateOfBirth" in traveler:
        date_of_birth = traveler["dateOfBirth"]
        passenger_details += f"Date of Birth: {date_of_birth}\n"

    passenger_type_code = traveler["passengerTypeCode"]

    passenger_details += f"Traveler First Name: {first_name}\n" \
                         f"Traveler Last Name: {last_name}\n" \
                         f"Traveler Prefix: {prefix}\n" \
                         f"Gender: {gender}\n" \
                         f"Passenger Type Code: {passenger_type_code}\n\n"

    # Extract flight details
    dictionaries = user_details["dictionaries"]
    dated_flight = dictionaries["datedFlight"]

    for flight_id, flight_details in dated_flight.items():
        flight_code = flight_id[:6]
        flight_date = flight_id[7:14]
        legs = flight_details["legs"]
        flight_points = flight_details["flightPoints"]

        passenger_details += f"Flight ID: {flight_id}\n"
        passenger_details += f"Flight Code: {flight_code}\n"
        passenger_details += f"Flight Date: {flight_date}\n"

        for leg in legs:
            board_point_iata_code = leg["boardPointIataCode"]
            off_point_iata_code = leg["offPointIataCode"]
            leg_dcs_statuses = leg["legDCSStatuses"]
            general_status = leg_dcs_statuses["generalStatus"]
            acceptance_status = leg_dcs_statuses["acceptanceStatus"]
            boarding_status = leg_dcs_statuses["boardingStatus"]
            baggage_status = leg_dcs_statuses["baggageStatus"]
            disruption_status = leg_dcs_statuses["disruptionStatus"]

            passenger_details += f"Board Point IATA Code: {board_point_iata_code}\n" \
                                 f"Off Point IATA Code: {off_point_iata_code}\n" \
                                 f"General Status: {general_status}\n" \
                                 f"Acceptance Status: {acceptance_status}\n" \
                                 f"Boarding Status: {boarding_status}\n" \
                                 f"Baggage Status: {baggage_status}\n" \
                                 f"Disruption Status: {disruption_status}\n"

        for flight_point in flight_points:
            iata_code = flight_point["iataCode"]
            if "departure" in flight_point:
                departure_timings = flight_point["departure"]["timings"]
                for departure_timing in departure_timings:
                    value = departure_timing["value"]
                    qualifier = departure_timing["qualifier"]
                    passenger_details += f"Departure Timing Value: {value}\n" \
                                         f"Departure Timing Qualifier: {qualifier}\n"
            if "arrival" in flight_point:
                arrival_timings = flight_point["arrival"]["timings"]
                for arrival_timing in arrival_timings:
                    value = arrival_timing["value"]
                    qualifier = arrival_timing["qualifier"]
                    passenger_details += f"Arrival Timing Value: {value}\n" \
                                         f"Arrival Timing Qualifier: {qualifier}\n"

    return passenger_details

