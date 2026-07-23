import asyncio
import random
from aiocoap import *
import aiocoap.resource as resource


class TemperatureResource(resource.Resource):

    async def render_get(self, request):

        temperature = round(random.uniform(20, 40), 1)

        print(f"Client Requested Temperature : {temperature} °C")

        payload = f"Temperature = {temperature}°C".encode("utf-8")

        return Message(payload=payload)


async def main():

    root = resource.Site()

    root.add_resource(
        ['temperature'],
        TemperatureResource()
    )

    await Context.create_server_context(root)

    print("===================================")
    print("      CoAP Server Started")
    print("===================================")
    print("Waiting for client requests...\n")

    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())