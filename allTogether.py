from dataclasses import dataclass
import json
import argparse
from typing import List
import requests


@dataclass
class Location:
    lat: float
    lng: float
    address: str
    city: str
    country: str


@dataclass
class Amenities:
    general: List[str]
    room: List[str]


@dataclass
class Image:
    link: str
    description: str


@dataclass
class Images:
    rooms: List[Image]
    site: List[Image]
    amenities: List[Image]


@dataclass
class Hotel:
    id: str
    destination_id: int
    name: str
    location: Location
    description: str
    amenities: Amenities
    images: Images
    booking_conditions: List[str]


class BaseSupplier:
    def endpoint(self) -> str:
        """URL to fetch supplier data."""
        raise NotImplementedError

    def parse(self, obj: dict) -> Hotel:
        """Parse supplier-provided data into a `Hotel` object."""
        raise NotImplementedError

    def fetch(self) -> List[Hotel]:
        """Fetch hotel data from the supplier and return a list of `Hotel` objects."""
        url = self.endpoint()
        response = requests.get(url)
        response.raise_for_status()  # Ensure successful response

        return [self.parse(dto) for dto in response.json()]


class Acme(BaseSupplier):
    @staticmethod
    def endpoint() -> str:
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme'

    @staticmethod
    def parse(dto: dict) -> Hotel:
        """Parse data from the Acme supplier into a Hotel object."""
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
                room=[],  # Example: adapt if room-level amenities are provided
            ),
            images=Images(
                rooms=[],  # Example: adapt if room images are provided
                site=[],  # Example: adapt if site images are provided
                amenities=[],  # Example: adapt if amenities images are provided
            ),
            booking_conditions=[],
        )


class Paperflies(BaseSupplier):
    def endpoint(self) -> str:
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies'

    def parse(self, dto: dict) -> Hotel:
        """Parse data from the Paperflies supplier into a Hotel object."""
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
                rooms=[Image(link=image["link"], description=image.get("caption", "")) for image in dto["images"].get("rooms", [])],
                site=[Image(link=image["link"], description=image.get("caption", "")) for image in dto["images"].get("site", [])],
                amenities=[],  # Example: adapt if amenities images are provided
            ),
            booking_conditions=dto.get("booking_conditions", []),
        )


class Patagonia(BaseSupplier):
    def endpoint(self) -> str:
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia'

    def parse(self, dto: dict) -> Hotel:
        """Parse data from the Patagonia supplier into a Hotel object."""
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
                room=[],  # Example: adapt if room-level amenities are provided
            ),
            images=Images(
                rooms=[Image(link=image["url"], description=image.get("description", "")) for image in dto["images"].get("rooms", [])],
                site=[],  # Example: adapt if site images are provided
                amenities=[Image(link=image["url"], description=image.get("description", "")) for image in dto["images"].get("amenities", [])],
            ),
            booking_conditions=dto.get("booking_conditions", []),
        )


class HotelsService:
    def __init__(self):
        self.data = []

    def merge_and_save(self, supplier_data: List[Hotel]):
        """Merge and deduplicate hotel data."""
        hotel_map = {}
        for hotel in supplier_data:
            if hotel.id not in hotel_map:
                hotel_map[hotel.id] = hotel
        self.data = list(hotel_map.values())

    def find(self, hotel_ids: List[str], destination_ids: List[int]) -> List[Hotel]:
        """Filter hotels by provided hotel_ids and destination_ids."""
        return [
            hotel for hotel in self.data
            if (not hotel_ids or hotel.id in hotel_ids) and
               (not destination_ids or hotel.destination_id in destination_ids)
        ]


def fetch_hotels(hotel_ids: List[str], destination_ids: List[int]) -> str:
    """Fetch, merge, and filter hotel data from multiple suppliers."""
    suppliers = [Acme(), Paperflies(), Patagonia()]

    # Fetch data from all suppliers
    all_supplier_data = []
    for supplier in suppliers:
        all_supplier_data.extend(supplier.fetch())

    # Merge and filter data
    svc = HotelsService()
    svc.merge_and_save(all_supplier_data)
    filtered = svc.find(hotel_ids, destination_ids)

    # Serialize to JSON and return
    return json.dumps([hotel.__dict__ for hotel in filtered], default=lambda o: o.__dict__, indent=4)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("hotel_ids", type=str, help="Comma-separated list of hotel IDs")
    parser.add_argument("destination_ids", type=str, help="Comma-separated list of destination IDs")
    args = parser.parse_args()

    hotel_ids = args.hotel_ids.split(",") if args.hotel_ids.lower() != "none" else []
    destination_ids = [int(d) for d in args.destination_ids.split(",")] if args.destination_ids.lower() != "none" else []
    return hotel_ids, destination_ids

def main():
    hotel_ids, destination_ids = parse_arguments()
    result = fetch_hotels(hotel_ids, destination_ids)
    print(result)



if __name__ == "__main__":
    main()


#./runner iJhz,f8c9 5432,1122
# python main.py iJhz,f8c9 5432,1122