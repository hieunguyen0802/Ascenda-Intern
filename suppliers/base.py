from abc import ABC, abstractmethod
from typing import List
from models.hotel import Hotel
import requests


class BaseSupplier(ABC):
    @abstractmethod
    def endpoint(self) -> str:
        """URL to fetch supplier data."""
        raise NotImplementedError

    @abstractmethod
    def parse(self, obj: dict) -> Hotel:
        """Parse supplier-provided data into a `Hotel` object."""
        raise NotImplementedError

    def fetch(self) -> List[Hotel]:
        """Fetch hotel data from the supplier and return a list of `Hotel` objects."""
        url = self.endpoint()
        response = requests.get(url)
        response.raise_for_status()
        return [self.parse(dto) for dto in response.json()]


class SupplierFactory:
    @staticmethod
    def get_suppliers() -> List[BaseSupplier]:
        """Return all available suppliers."""
        from suppliers.acme import Acme
        from suppliers.paperflies import Paperflies
        from suppliers.patagonia import Patagonia
        return [Acme(), Paperflies(), Patagonia()]
