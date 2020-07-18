from src.lib.Location import Address
from src.lib.Extractor import MultiLayer
import asyncio


async def main():
    data = MultiLayer(29.798146, -97.071763, base_dir="./layer/Re_Lower_Colorado_buffered").extract()
    print(data)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
