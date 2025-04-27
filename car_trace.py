import csv
import datetime
import logging
import pathlib
import typing
import collections

from agent import GeoClient, Point

logging.basicConfig(level=logging.INFO)

EXPECTED_HEADER = {"end_time" ,"m_tmsi", "pos_last_lon" ,"pos_last_lat"}
RECORD_LOCATIONS = collections.defaultdict(list)

geo_agent = GeoClient("car-trace")



def load_data(path: pathlib.Path, batch_size=1000) -> typing.Iterable[str]:
    if not path.exists():
        raise ValueError(f"File {path} does not exist.")

    with open(path) as f:
        data = csv.DictReader(f)
        header = set(data.fieldnames)

        if not EXPECTED_HEADER.issubset(header):
            missing_fields = EXPECTED_HEADER - header
            raise ValueError(
                f"Invalid header: missing required fields {missing_fields}. Expected {EXPECTED_HEADER}, got {header}")

        batch = []
        for row in data:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:
            yield batch


def extract_address_from_data(data: typing.List[str]) -> str:
    for row in data:
        lat, lon = row['pos_last_lat'], row['pos_last_lon']
        try:
            address = geo_agent.get_address_from_coordinates(lat, lon)
        except Exception as e:
            raise e
    return address


def record_location_by_tmsi(data: typing.Iterable[typing.List[str]], max_records_per_tmsi=1000):
    max_speed, max_distance, accumulate_distance = 0.0, 0.0, 0.0
    bolt = ""

    for chunk in data:
        for row in chunk:
            tmsi = str(row.get('m_tmsi', None))
            end_time = datetime.datetime.strptime(row.get('end_time', None),"%Y-%m-%d %H:%M:%S")
            lat = float(row.get('pos_last_lat', 0.0))
            lon = float(row.get('pos_last_lon', 0.0))
            point = Point(lat, lon)

            if tmsi in RECORD_LOCATIONS:
                previous_point = Point(previous_lat, previous_lon)
                distance = geo_agent.get_distance_in_kilometers(previous_point, point)
                accumulate_distance += distance
                time_range = (end_time - previous_end_time).total_seconds() / 3600.0
                speed = distance / time_range if time_range > 0 else 0.0
                collection = { "time_range": time_range, "distance": distance, "speed": speed}

                if speed > max_speed:
                    max_speed = speed
                    bolt = tmsi

                if accumulate_distance > max_distance:
                    max_distance = accumulate_distance

                RECORD_LOCATIONS[tmsi].append(collection)
            else:
                previous_lat, previous_lon = point.lat, point.lon
                previous_end_time = end_time
                distance, time_range, speed = 0.0, 0.0, 0.0
                collection = { "time_range": time_range, "distance": distance, "speed": speed }
                RECORD_LOCATIONS[tmsi]= [collection]

    logging.info(f"Max speed: {max_speed} km/h")
    logging.info(f"Usain Bolt: {bolt}")
    logging.info(f"Max distance: {max_distance} km")
    return RECORD_LOCATIONS


def main(str_path: str = "data/car-trace-large.csv"):
    try:
        data = load_data(pathlib.Path(str_path))
        records = record_location_by_tmsi(data)
        return records
    except Exception as e:
        logging.error(e)
        return None

if __name__ == "__main__":
    str_path: str = "data/car-trace-large.csv"
    main(str_path)

