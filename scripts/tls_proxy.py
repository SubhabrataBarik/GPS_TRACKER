"""
Standalone TLS-terminating TCP proxy for local LAN/mobile testing.

Terminates HTTPS/WSS on LISTEN_PORT using the self-signed dev cert in
certs/, and relays the raw bytes to the plain HTTP backend (Daphne via
`manage.py runserver`) on BACKEND_PORT. Works for both REST calls and
WebSocket upgrades since it proxies at the TCP level, below HTTP.

Exists because daphne's native `-e ssl:...` endpoint currently crashes
on every connection due to a pyOpenSSL/Twisted ALPN incompatibility
(see conversation history) -- this sidesteps that entirely.

Usage: python scripts/tls_proxy.py
"""

import asyncio
import ssl
from pathlib import Path

LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 8000
BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 8001

CERT_DIR = Path(__file__).resolve().parent.parent / "certs"
CERT_FILE = CERT_DIR / "dev-cert.pem"
KEY_FILE = CERT_DIR / "dev-key.pem"


async def pump(reader, writer):
    try:
        while True:
            data = await reader.read(65536)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except (ConnectionResetError, BrokenPipeError):
        pass
    finally:
        writer.close()


async def handle_client(client_reader, client_writer):
    try:
        backend_reader, backend_writer = await asyncio.open_connection(
            BACKEND_HOST, BACKEND_PORT,
        )
    except OSError:
        client_writer.close()
        return

    await asyncio.gather(
        pump(client_reader, backend_writer),
        pump(backend_reader, client_writer),
    )


async def main():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(str(CERT_FILE), str(KEY_FILE))

    server = await asyncio.start_server(
        handle_client, LISTEN_HOST, LISTEN_PORT, ssl=ssl_context,
    )

    print(f"TLS proxy: https://<your-lan-ip>:{LISTEN_PORT} -> http://{BACKEND_HOST}:{BACKEND_PORT}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
