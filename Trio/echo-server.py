# echo-server.py

import trio
from itertools import count


PORT = 12345
BUFSIZE = 16384


CONNECTION_COUNTER = count()


async def echo_server(server_stream):
    ident = next(CONNECTION_COUNTER)
    print(f"echo_server {ident}: starting")
    try:
        while True:
            data = await server_stream.receive_some(BUFSIZE)
            print(f"echo_server {ident}: received {data}")
            if not data:
                print("closing connection")
                return
            print(f"echo_server {ident}: sending {data}")
            await server_stream.send_all(data)
    except Exception as exc:
        print(f"echo_server {ident}: crashed: {exc}")


async def main():
    await trio.serve_tcp(echo_server, PORT)


trio.run(main)
