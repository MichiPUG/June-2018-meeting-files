# echo-client.py

import sys
import trio
from uuid import uuid4 as random_uuid


PORT = 12345
BUFSIZE = 16384


async def sender(client_stream):
    print("sender: starting")
    while True:
        data = random_uuid().urn[9:].encode()
        print(f"sender: sending {data}")
        await client_stream.send_all(data)
        await trio.sleep(0.15)


async def receiver(client_stream):
    print("receiver: starting")
    while True:
        data = await client_stream.receive_some(BUFSIZE)
        if not data:
            print("closing connection")
            sys.exit()
        print(f"receiver: got {data}")


async def main():
    print(f"main: opening TCP stream 127.0.0.1:{PORT}")
    client_stream = await trio.open_tcp_stream("127.0.0.1", PORT)
    async with trio.open_nursery() as nursery:
        print("main: spawning sender...")
        nursery.start_soon(sender, client_stream)
        print("main: spawning receiver...")
        nursery.start_soon(receiver, client_stream)


trio.run(main)
