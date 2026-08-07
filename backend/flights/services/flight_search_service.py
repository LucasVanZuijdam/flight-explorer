from flights.models import Airport, FlightOffer
from flights.providers.mock_provider import search_flights


def run_flight_search(search):
    raw_offers = search_flights(
        origin=search.origin.iata_code,
        departure_date=search.departure_date,
        return_date=search.return_date,
    )

    saved_offers = []

    for raw_offer in raw_offers:
        destination = Airport.objects.get(
            iata_code=raw_offer["destination"]
        )

        offer = FlightOffer.objects.create(
            search=search,
            origin=search.origin,
            destination=destination,
            airline=raw_offer["airline"],
            price=raw_offer["price"],
        )

        saved_offers.append(offer)

    return saved_offers