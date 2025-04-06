from geopy.geocoders import Nominatim

# Initialize Geopy's geocoder
geolocator = Nominatim(user_agent="househunt")


# TODO: make this better
def normalize_address(address: str) -> dict[str, str]:
    """Normalize the address using Geopy and return a dict with address components"""

    location = geolocator.geocode(address, country_codes=["us"], addressdetails=True)

    if location:
        return {
            "address": location.address,  # type: ignore
            "latitude": location.latitude,  # type: ignore
            "longitude": location.longitude,  # type: ignore
            "city": location.raw.get("address", {}).get("city", ""),  # type: ignore
            "state": location.raw.get("address", {}).get("state", ""),  # type: ignore
            "zipcode": location.raw.get("address", {}).get("postcode", ""),  # type: ignore
            "place_id": location.raw["place_id"],  # type: ignore
        }

    else:
        raise ValueError(
            "Could not geocode the address. Please check the address input."
        )
