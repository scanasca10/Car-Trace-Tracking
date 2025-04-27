from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy import distance


class Point:
    def __init__(self, latitude, longitude):
        self.lat = latitude
        self.lon = longitude


class GeoClient:
    def __init__(self, user_agent, min_delay=1):
        self.user_agent = user_agent
        self.geolocator = Nominatim(user_agent=self.user_agent)
        self.reverse_geocode = RateLimiter(
            self.geolocator.reverse,
            min_delay_seconds=min_delay
        )

    def get_address_from_coordinates(self, latitude, longitude) -> str | None :
        query = f"{latitude},{longitude}"
        location = self.reverse_geocode(query)
        if location:
            return location.address
        else:
            return None

    @staticmethod
    def get_distance_in_kilometers(previous_point: Point, current_point: Point) -> float | None:
        previous_point = (previous_point.lat, previous_point.lon)
        current_point = (current_point.lat, current_point.lon)

        return distance.distance(previous_point, current_point).km


