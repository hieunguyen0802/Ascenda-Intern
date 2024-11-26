# suppliers/acme.py

from suppliers.base import BaseSupplier
from models.hotel import Hotel, Location, Amenities, Images

class Acme(BaseSupplier):
    def endpoint(self) -> str:
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme'

    def parse(self, dto: dict) -> Hotel:
        return Hotel(
            id=dto["Id"],
            destination_id=dto["DestinationId"],
            name=dto["Name"],
            location=Location(
                lat=dto.get("Latitude", 0.0),
                lng=dto.get("Longitude", 0.0),
                address=dto.get("Address", ""),
                city=dto.get("City", ""),
                country=dto.get("Country", ""),
            ),
            description=dto.get("Description", ""),
            amenities=Amenities(
                general=dto.get("Facilities", []),
                room=[],
            ),
            images=Images(
                rooms=[],
                site=[],
                amenities=[],
            ),
            booking_conditions=[],
        )
