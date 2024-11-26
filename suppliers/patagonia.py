from suppliers.base import BaseSupplier
from models.hotel import Hotel, Location, Amenities, Images, Image


class Patagonia(BaseSupplier):
    def endpoint(self) -> str:
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia'

    def parse(self, dto: dict) -> Hotel:
        return Hotel(
            id=dto["id"],
            destination_id=int(dto["destination"]),
            name=dto["name"],
            location=Location(
                lat=dto.get("lat", 0.0),
                lng=dto.get("lng", 0.0),
                address=dto.get("address", ""),
                city=dto.get("city", ""),
                country=dto.get("country", ""),
            ),
            description=dto.get("info", ""),
            amenities=Amenities(
                general=dto.get("amenities", []),
                room=[],
            ),
            images=Images(
                rooms=[
                    Image(link=image["url"], description=image.get("description", ""))
                    for image in dto["images"].get("rooms", [])
                ],
                site=[],
                amenities=[
                    Image(link=image["url"], description=image.get("description", ""))
                    for image in dto["images"].get("amenities", [])
                ],
            ),
            booking_conditions=dto.get("booking_conditions", []),
        )
