import glob
import os
import time
import numpy
import rasterio as rio
from rasterio.windows import Window
from pydantic import BaseModel
from typing import List
from logging import info
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from src.models.Pixel import SeriesValuePixel, SingleValuePixel
from src.models.Location import Coordinate


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
            start = time.time()
            for i in range(1, dataset.count):
                try:
                    pixel_value = dataset.read(i, window=window)[index]
                except IndexError:
                    pixel_value = dataset.read(i)[index]
                pixel_series.append(pixel_value)

            end = time.time()
            info(f"process time: {end - start} second")
            info(f"Pixel Value: {pixel_series} ")
            if len(pixel_series) == 1:
                return SingleValuePixel(
                    coordinate=Coordinate(latitude=self.latitude, longitude=self.longitude), value=pixel_series[0],
                    layer=self.tif
                )
            else:
                return SeriesValuePixel(
                    coordinate=Coordinate(latitude=self.latitude, longitude=self.longitude), values=pixel_series,
                    layer=self.tif
                )


class MultiLayer(ExtractorInterface):
    def extract(self):
        pass


class StackLayer(ExtractorInterface):
    def extract(self):
        pass
