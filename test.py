from src.lib.Location import Address
import asyncio


async def main():
    data = Address("Sari")
    await data.initialise()
    print(data.information())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
