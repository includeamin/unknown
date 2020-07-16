import glob
import os
import rasterio as rio
from rasterio.windows import Window
from typing import List
from logging import info
from src.models.Pixel import SeriesValuePixel, SingleValuePixel
from src.models.Location import Coordinate
from src.lib.ReProject import ToEPSG4326, ProjectionTools


class ExtractorInterface:
    def extract(self):
        pass


class SingleLayer(ExtractorInterface):
    def __init__(self, latitude: float, longitude: float, tif: str):
        self.latitude = latitude
        self.longitude = longitude
        self.tif = tif

    def extract(self) -> SeriesValuePixel or SingleValuePixel:
        with rio.open(self.tif, "r") as dataset:
            index = dataset.index(self.longitude, self.latitude)
            window = Window(index[1] - 1, index[0] - 1, index[1] + 1, index[0] + 1)
            pixel_series = []
            for i in range(1, dataset.count + 1):
                try:
                    pixel_value = dataset.read(i, window=window)[index]
                except IndexError:
                    pixel_value = dataset.read(i)[index]
                pixel_series.append(pixel_value)

            if len(pixel_series) == 1:
                return SingleValuePixel(
                    coordinate=Coordinate(
                        latitude=self.latitude, longitude=self.longitude
                    ),
                    value=pixel_series[0],
                    layer=self.tif,
                )
            else:
                return SeriesValuePixel(
                    coordinate=Coordinate(
                        latitude=self.latitude, longitude=self.longitude
                    ),
                    values=pixel_series,
                    layer=self.tif,
                )


class MultiLayer(ExtractorInterface):
    def __init__(self, latitude: float, longitude: float, base_dir: str):
        self.latitude = latitude
        self.longitude = longitude
        self.base_dir = base_dir

    def extract(self):
        results: List[SingleValuePixel] = []
        layer_list = os.listdir(self.base_dir)
        for layer in layer_list:
            if layer == "WSB":
                continue
            # Assume we have only one tif in every layer directory
            tif = glob.glob(os.path.join(self.base_dir, layer, "*.tif"))[0]
            info(f"processing {layer} layer ...")
            if ProjectionTools.is_epsg_4326(tif):
                info("Coordinate Reference system is not EPSG:4326")
                info("Change Projection to EPSG:4326")
                result_path = ToEPSG4326(tif).convert()
                result = SingleLayer(
                    self.latitude, self.longitude, result_path
                ).extract()

            else:
                info("Coordinate Reference system is EPSG:4326")
                result = SingleLayer(self.latitude, self.longitude, tif).extract()
            results.append(result)
        return results
