# from src.lib.Location import Address
from src.lib.Extractor import SingleLayer
from src.lib.Extractor import S3MultiLayer

path = "s3://bigdata/Layer_Stack/Chia/Chla_05-Jul-16_20-Aug-18.tif"

from src.lib.StorageManager import StorageManagement

# res = (
#     SingleLayer(
#         29.798146,
#         -97.071763,
#         tif="s3://bigdata/Layer_Stack/Chia/flood_hazard_1000m_buffered.tif",
#     )
#     .apply_s3(s3=StorageManagement())
#     .s3_extractor()
# )
#
# print(res)

# from src.lib.Location import Address
import asyncio


async def main():
    ml = S3MultiLayer(29.798146,
                      -97.071763, "Layer/", StorageManagement())
    result = await ml.s3_extract()
    print(result)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
