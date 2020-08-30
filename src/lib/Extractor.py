import glob
import os
import rasterio as rio
from rasterio.windows import Window
from typing import List, Optional, AsyncIterable
from logging import info

from src.lib.StorageManager import StorageManagement
from src.models.Pixel import SeriesValuePixel, SingleValuePixel
from src.models.Location import Coordinate
from src.lib.ReProject import ToEPSG4326, ProjectionTools
from rasterio.fill import fillnodata
from rasterio.mask import mask


class ExtractorInterface:
    def extract(self):
        pass


class SingleLayer(ExtractorInterface):
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


# class MultiLayer(ExtractorInterface):
#     def __init__(self, latitude: float, longitude: float, base_dir: str):
#         self.latitude = latitude
#         self.longitude = longitude
#         self.base_dir = base_dir
#
#     def extract(self):
#         results: List[SingleValuePixel] = []
#         layer_list = os.listdir(self.base_dir)
#         for layer in layer_list:
#             if layer == "WSB":
#                 continue
#             # Assume we have only one tif in every layer directory
#             tif = glob.glob(os.path.join(self.base_dir, layer, "*.tif"))[0]
#             info(f"processing {layer} layer ...")
#             if ProjectionTools.is_epsg_4326(tif):
#                 info("Coordinate Reference system is not EPSG:4326")
#                 info("Change Projection to EPSG:4326")
#                 result_path = ToEPSG4326(tif).convert()
#                 result = SingleLayer(
#                     self.latitude, self.longitude, result_path
#                 ).extract()
#
#             else:
#                 info("Coordinate Reference system is EPSG:4326")
#                 result = SingleLayer(self.latitude, self.longitude, tif).extract()
#             results.append(result)
#         return results
#
#
# class S3MultiLayer(ExtractorInterface):
#     def __init__(
#         self,
#         latitude: float,
#         longitude: float,
#         base_dir: str,
#         storage: StorageManagement,
#     ):
#         self.latitude = latitude
#         self.longitude = longitude
#         self.base_dir = base_dir
#         self._storage = storage
#
#     async def extract(self) -> List[SingleValuePixel]:
#         results: List[SingleValuePixel] = []
#         if self._storage.forced_path:
#             result = await (
#                 SingleLayer(
#                     self.latitude, self.longitude, self._storage.get_storage_path()
#                 )
#                 .apply_s3(self._storage)
#                 .s3_extractor()
#             )
#             results.append(result)
#         else:
#             layer_list = await self._storage.get_list_of_tiffs(self.base_dir)
#             for layer in layer_list:
#                 if layer.__contains__("WSB"):
#                     continue
#                 result = await (
#                     SingleLayer(self.latitude, self.longitude, layer)
#                     .apply_s3(self._storage)
#                     .s3_extractor()
#                 )
#                 results.append(result)
#
#         return results
