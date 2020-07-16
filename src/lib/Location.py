from src.models.Location import AddressString, AddressInformation, Coordinate
from geopy.geocoders import Nominatim
from src.settings.Settings import location_settings


class Address:
    location = None

    def __init__(self, address: str):
        self.address = AddressString(address=address)

    async def initialise(self):
        geo_locator = Nominatim(user_agent=location_settings.AGENT_NAME)
        self.location = geo_locator.geocode(self.address.address)

    def information(self):
        if not self.location:
            raise Exception("location not initialised")
        return AddressInformation(
            full_address=str(self.location),
            coordinate=Coordinate(
                latitude=self.location.latitude, longitude=self.location.longitude
            ),
        )
