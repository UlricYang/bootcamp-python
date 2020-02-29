import asyncio

import aiohttp

import aiosocks
from aiosocks.connector import ProxyClientRequest, ProxyConnector


async def load_github_main():
    auth5 = aiosocks.Socks5Auth("proxyuser1", password="pwd")
    ba = aiohttp.BasicAuth("login")

    # remote resolve
    conn = ProxyConnector(remote_resolve=True)

    # or locale resolve
    conn = ProxyConnector(remote_resolve=False)

    try:
        with aiohttp.ClientSession(connector=conn, request_class=ProxyClientRequest) as session:
            # socks5 proxy
            async with session.get(
                "http://github.com/", proxy="socks5://127.0.0.1:1080", proxy_auth=auth5
            ) as resp:
                if resp.status == 200:
                    print(await resp.text())
            # http proxy
            async with session.get(
                "http://github.com/", proxy="http://127.0.0.1:8080", proxy_auth=ba
            ) as resp:
                if resp.status == 200:
                    print(await resp.text())
    except aiohttp.ClientProxyConnectionError:
        # connection problem
        print("communication problem")
    except aiohttp.ClientConnectorError:
        # ssl error, certificate error, etc
        print("ssl error, certificate error, etc")
    except aiosocks.SocksError:
        # communication problem
        print("communication problem")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(load_github_main())
    loop.close()
