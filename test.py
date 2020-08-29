# # from src.lib.Location import Address
# from src.lib.Extractor import SingleLayer
# from src.lib.Extractor import S3MultiLayer
#
# path = "s3://bigdata/Layer_Stack/Chia/Chla_05-Jul-16_20-Aug-18.tif"
#
# from src.lib.StorageManager import StorageManagement
# import asyncio
#
#
# # res = (
# #     SingleLayer(
# #         29.798146,
# #         -97.071763,
# #         tif="s3://bigdata/Layer_Stack/Chia/flood_hazard_1000m_buffered.tif",
# #     )
# #     .apply_s3(s3=StorageManagement())
# #     .s3_extractor()
# # )
# #
# # print(res)
#
# # from src.lib.Location import Address
#
#
# async def main():
#     ml = S3MultiLayer(29.798146, -97.071763, "Layer/", StorageManagement())
#     result = await ml.extract()
#     print(result)
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())


from pymongo import MongoClient
from pydantic import BaseModel
from src.models.Location import Coordinate

collection = MongoClient("mongodb://localhost:27017").get_database("test").get_collection("geo")


class Pixel(BaseModel):
    location = {"type": 'Point', "coordinate": []}
    type: str = 'single'
    value: float
