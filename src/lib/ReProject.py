import rasterio as rio
from src.lib.PathManager import PathManager
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling


class ProjectionTools:
    @staticmethod
    def is_epsg_4326(tif):
        with rio.open(tif, "r") as dataset:
            if dataset.crs != "EPSG:4326":
                return True
            return False


class ReProjectInterface:
    def convert(self):
        pass


class ToEPSG4326(ReProjectInterface):
    def __init__(self, tif: str):
        self.tif = tif

    def convert(self):
        dst_crs = "EPSG:4326"
        result_path = PathManager.create_out_put(self.tif)

        with rasterio.open(self.tif) as src:
            transform, width, height = calculate_default_transform(
                src.crs, dst_crs, src.width, src.height, *src.bounds
            )
            kwargs = src.meta.copy()
            kwargs.update(
                {
                    "crs": dst_crs,
                    "transform": transform,
                    "width": width,
                    "height": height,
                }
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
