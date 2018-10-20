import re
import os
from uuid import uuid1

import asyncpg
import aiofiles
from bs4 import BeautifulSoup
import tornado.httpclient

from settings import POSTGRES, DOWNLOAD_DIR, DOWNLOAD_DIR_NAME, HOST, PROTOCOL


def parse_og_tags(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.html.head.find_all(property=re.compile(r'^og'))

    data = {}
    for tag in tags:
        _property = tag.get('property', None)
        content = tag.get('content', None)
        if _property is None or content is None:
            continue

        name = _property.split(':')[-1]
        content = content.strip()
        data[name] = content

    return data


async def process_url(url: str):
    http = tornado.httpclient.AsyncHTTPClient()
    response = await http.fetch(url)
    data = parse_og_tags(response.body)
    return data


async def load_image(url: str):
    http = tornado.httpclient.AsyncHTTPClient()
    response = await http.fetch(url)

    name = str(uuid1())
    path = os.path.join(DOWNLOAD_DIR, name)
    async with aiofiles.open(path, 'wb') as f:
        await f.write(response.body)

    return '{}://{}/{}/{}'.format(PROTOCOL, HOST, DOWNLOAD_DIR_NAME, name)


async def make_connection():
    return await asyncpg.connect(**POSTGRES)
