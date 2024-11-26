from suppliers.base import BaseSupplier
from models.hotel import Hotel, Location, Amenities, Images, Image


class Paperflies(BaseSupplier):
    def endpoint(self) -> str:
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies'

    def parse(self, dto: dict) -> Hotel:
        return Hotel(
            id=dto["hotel_id"],
            destination_id=int(dto["destination_id"]),
            name=dto["hotel_name"],
            location=Location(
                address=dto.get("location", {}).get("address", ""),
                country=dto.get("location", {}).get("country", ""),
                lat=dto.get("Latitude", 0.0),
                lng=dto.get("Longitude", 0.0),
                city=dto.get("City", ""),
            ),
            description=dto.get("details", ""),
            amenities=Amenities(
                general=dto.get("amenities", {}).get("general", []),
                room=dto.get("amenities", {}).get("room", []),
            ),
            images=Images(
                rooms=[
                    Image(link=image["link"], description=image.get("caption", ""))
                    for image in dto["images"].get("rooms", [])
                ],
                site=[
                    Image(link=image["link"], description=image.get("caption", ""))
                    for image in dto["images"].get("site", [])
                ],
                amenities=[],
            ),
            booking_conditions=dto.get("booking_conditions", []),
        )
