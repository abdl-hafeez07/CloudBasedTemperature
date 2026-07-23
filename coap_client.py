import asyncio
from aiocoap import *


async def main():

    protocol = await Context.create_client_context()

    request = Message(
        code=GET,
        uri="coap://localhost/temperature"
    )

    response = await protocol.request(request).response

    print("Server Response:")
    print(response.payload.decode())


if __name__ == "__main__":
    asyncio.run(main())