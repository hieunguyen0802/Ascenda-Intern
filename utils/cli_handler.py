import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("hotel_ids", type=str, help="Comma-separated list of hotel IDs")
    parser.add_argument("destination_ids", type=str, help="Comma-separated list of destination IDs")
    args = parser.parse_args()

    hotel_ids = args.hotel_ids.split(",") if args.hotel_ids.lower() != "none" else []
    destination_ids = [int(d) for d in args.destination_ids.split(",")] if args.destination_ids.lower() != "none" else []
    return hotel_ids, destination_ids
