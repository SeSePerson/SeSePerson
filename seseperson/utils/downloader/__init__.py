import aiohttp
from aiohttp import ClientTimeout

from .exceptions import FileTooLargeError


async def download_url(url, max_size=32 * 1024 * 1024, timeout=20):
    timeout = ClientTimeout(total=timeout)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as response:
            if response.status != 200:
                response.raise_for_status()

            data = bytearray()
            async for chunk in response.content.iter_chunked(1024):
                # noinspection PyTypeChecker
                data.extend(chunk)
                if len(data) > max_size:
                    raise FileTooLargeError("File size exceeds.")
            return data
