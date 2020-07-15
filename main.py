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
from pprint import pprint

"""
unusable code
just proof of concept
"""
"""
| x' |   | a b c | | x |
| y' | = | d e f | | y |
| 1  |   | 0 0 1 | | 1 |

x' world coordinate = Long
y' world coordinate = Lat
x image coordinate
y image coordinate
Long = X, Lat = Y

Google map and Google earth latitude, longitude order longitude,latitude
Coordinate Reference System = EPSG:4326
EPSG:4326 specifically states that the coordinate order should be latitude, longitude.
"""


class SingleValuePixel(BaseModel):
    tif: str
    latitude: float
    longitude: float
    value: float


class SeriesValuePixel(BaseModel):
    tif: str
    latitude: float
    longitude: float
    value: List[float]


def single_layer(lat, long, infile):
    with rio.open(infile, "r") as dataset:
        index = dataset.index(long, lat)
        window = Window(index[1] - 1, index[0] - 1, index[1] + 1, index[0] + 1)
        start = time.time()
        try:
            pixel_value = dataset.read(1, window=window)[index]
        except IndexError:
            pixel_value = dataset.read(1)[index]
        end = time.time()
        info(f"process time: {end - start} second")
        info(f"Pixel Value: {pixel_value} ")
        if isinstance(pixel_value, list):
            return SeriesValuePixel(
                latitude=lat, longitude=long, value=pixel_value, tif=infile
            )
        elif (
            isinstance(pixel_value, numpy.int8)
            or isinstance(pixel_value, numpy.float32)
            or isinstance(pixel_value, numpy.uint16)
            or isinstance(pixel_value, numpy.int32)
        ):
            return SingleValuePixel(
                latitude=lat, longitude=long, value=pixel_value, tif=infile
            )
        else:
            raise ValueError(f"Unknown PixelValue {pixel_value}")


def stack_layer(lat: float, long: float):
    pass


def change_projection(tif: str):
    dst_crs = "EPSG:4326"
    result_path = create_out_put(tif)

    with rasterio.open(tif) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds
        )
        kwargs = src.meta.copy()
        kwargs.update(
            {"crs": dst_crs, "transform": transform, "width": width, "height": height}
        )

        with rasterio.open(result_path, "w", **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest,
                )
    return result_path


def create_out_put(tif: str, base: str = "./out"):
    dirs = tif.split("/")[1:]
    dirs_list = [base]
    dirs_list.extend(dirs[:-1])
    new_path = os.path.join(*dirs_list)
    info(f"new path has been created: {new_path}")
    tif_path = os.path.join(new_path, dirs[-1])
    # Check is path exist or not
    if os.path.exists(tif_path):
        return tif_path
    if os.path.isdir(new_path):
        return tif_path
    os.makedirs(new_path)
    return tif_path


def should_change_projection(tif):
    with rio.open(tif, "r") as dataset:
        if dataset.crs != "EPSG:4326":
            return True
        return False


def multi_layer(lat, long, base_dir: str) -> List[SingleValuePixel]:
    results: List[SingleValuePixel] = []
    layer_list = os.listdir(base_dir)
    for layer in layer_list:
        if layer == "WSB":
            continue
        # Assume we have only one tif in every layer directory
        tif = glob.glob(os.path.join(base_dir, layer, "*.tif"))[0]
        info(f"processing {layer} layer ...")
        if should_change_projection(tif):
            info("Coordinate Reference system is not EPSG:4326")
            info("Change Projection to EPSG:4326")
            result_path = change_projection(tif)
            result = single_layer(lat, long, result_path)

        else:
            info("Coordinate Reference system is EPSG:4326")
            result = single_layer(lat, long, tif)
        results.append(result)
    return results


if __name__ == "__main__":
    output = multi_layer(
        29.798146, -97.071763, base_dir="./layer/Lower_Colorado_buffered"
    )
    pprint(output)
