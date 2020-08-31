import rasterio as rio
from rasterio.windows import Window
from src.lib.StorageManager import StorageManagement
from src.models.Pixel import SeriesValuePixel, SingleValuePixel
from src.models.Location import Coordinate
from rasterio.fill import fillnodata


class SingleLayer:
    _s3: StorageManagement = None

    def __init__(self, latitude: float, longitude: float, tif: str):
        self.latitude = latitude
        self.longitude = longitude
        self.tif = tif
        self._fill_nodata: bool = False

    def extract(self) -> SeriesValuePixel or SingleValuePixel:
        with rio.open(self.tif, "r") as dataset:
            return self._process(dataset)

    def apply_s3(self, s3: StorageManagement):
        self._s3 = s3
        return self

    async def s3_extractor(self):
        if not self._s3:
            raise Exception("S3 Storage Not Applied")
        with self._s3.ENV:
            with rio.open(self._s3.get_storage_path(self.tif)) as dataset:
                return self._process(dataset)

    def fill_nodata(self):
        self._fill_nodata = True
        return self

    def _process(self, dataset):
        index = dataset.index(self.longitude, self.latitude)
        window = Window(index[1] - 1, index[0] - 1, index[1] + 1, index[0] + 1)
        pixel_series = []
        for i in range(1, dataset.count + 1):
            try:
                image_array = dataset.read(i, window=window)
                if self._fill_nodata:
                    fillnodata(image_array, mask=dataset.read_masks(1))
                pixel_value = image_array[index]
            except IndexError:
                pixel_value = dataset.read(i)[index]
            pixel_series.append(pixel_value)

        if len(pixel_series) == 1:
            return SingleValuePixel(
                coordinate=Coordinate(latitude=self.latitude, longitude=self.longitude),
                value=pixel_series[0],
                layer=self.tif,
            )
        else:
            return SeriesValuePixel(
                coordinate=Coordinate(latitude=self.latitude, longitude=self.longitude),
                values=[float(item) for item in pixel_series],
                layer=self.tif,
            )
