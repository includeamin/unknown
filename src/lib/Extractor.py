class ExtractorInterface:
    def extract(self):
        pass


class SingleLayer(ExtractorInterface):
    def __init__(self, latitude: float, longitude: float, tif: str):
        self.latitude = latitude
        self.longitude = longitude
        self.tif = tif

    def extract(self):
        pass


class MultiLayer(ExtractorInterface):
    def extract(self):
        pass


class StackLayer(ExtractorInterface):
    def extract(self):
        pass
