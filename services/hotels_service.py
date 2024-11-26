from typing import List
from models.hotel import Hotel


class HotelsService:
    def __init__(self, suppliers):
        self.suppliers = suppliers
        self.data = []

    def fetch_and_merge(self):
        """Fetch data from suppliers and merge it."""
        all_supplier_data = []
        for supplier in self.suppliers:
            all_supplier_data.extend(supplier.fetch())
        self.merge_and_save(all_supplier_data)

    def merge_and_save(self, supplier_data: List[Hotel]):
        """Merge and deduplicate hotel data."""
        hotel_map = {hotel.id: hotel for hotel in supplier_data}
        self.data = list(hotel_map.values())

    def find(self, hotel_ids: List[str], destination_ids: List[int]) -> List[Hotel]:
        """Filter hotels by provided hotel_ids and destination_ids."""
        return [
            hotel for hotel in self.data
            if (not hotel_ids or hotel.id in hotel_ids) and
               (not destination_ids or hotel.destination_id in destination_ids)
        ]
