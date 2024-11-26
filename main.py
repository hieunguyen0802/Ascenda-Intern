from utils.cli_handler import parse_arguments
from services.hotels_service import HotelsService
from suppliers.base import SupplierFactory
import json

def main():
    # Parse arguments
    hotel_ids, destination_ids = parse_arguments()

    # Fetch data from suppliers
    suppliers = SupplierFactory.get_suppliers()
    svc = HotelsService(suppliers)
    svc.fetch_and_merge()
    filtered_hotels = svc.find(hotel_ids, destination_ids)

    # Output results as JSON
    print(json.dumps([hotel.__dict__ for hotel in filtered_hotels], default=lambda o: o.__dict__, indent=4))


if __name__ == "__main__":
    main()
