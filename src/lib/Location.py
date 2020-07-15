from src.models.Address import AddressString
from geopy.geocoders import Nominatim
from src.settings.Settings import location_settings
from geopy.adapters import AioHTTPAdapter


class Address:
    location = None

    def __init__(self, address: str):
        self.address = AddressString(address=location_settings.AGENT_NAME)

    async def initialise(self):
        async with Nominatim(
            user_agent=location_settings.AGENT_NAME, adapter_factory=AioHTTPAdapter,
        ) as geo_locator:
            self.location = await geo_locator.geocode(self.address)

    def information(self):
        if not self.location:
            raise Exception("location not initialised")
        print(self.location.__doc__)
