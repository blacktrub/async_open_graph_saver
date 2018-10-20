import json

import tornado.ioloop
import tornado.web
import tornado.escape

import settings
from constants import MAX_URLS_COUNT, REQUIRED_TAGS
from utils import process_url, make_connection, load_image


class LinksSaverHandler(tornado.web.RequestHandler):
    @staticmethod
    def validate(data: dict) -> bool:
        # todo: maybe need validate urls

        if 'urls' not in data:
            return False

        links = data['urls']
        if not isinstance(links, list):
            return False

        if len(links) > MAX_URLS_COUNT:
            return False

        return True

    async def post(self, *args, **kwargs):
        try:
            data = tornado.escape.json_decode(self.request.body)
        except json.JSONDecodeError:
            raise tornado.web.HTTPError(
                status_code=400,
                log_message='bad json',
            )

        if not self.validate(data):
            raise tornado.web.HTTPError(
                status_code=400,
                log_message='bad json',
            )

        links = []
        connection = await make_connection()
        try:
            exists_links = await connection.fetch(
                'SELECT * FROM links WHERE url = ANY ($1::text[])', list(data['urls']),
            )

            exists_links_urls = []
            for exist_link in exists_links:
                links.append(dict(exist_link))
                exists_links_urls.append(exist_link['url'])

            new_urls = [u for u in data['urls'] if u not in exists_links_urls]
            for url in new_urls:
                data = await process_url(url)
                if not all(t in data for t in REQUIRED_TAGS):
                    continue

                image = await load_image(data['image'])

                link_id = await connection.fetchval(
                    'INSERT INTO links(url, title, description, image) VALUES ($1, $2, $3, $4) RETURNING id',
                    url, data['title'], data['description'], image
                )
                links.append({
                    'id': int(link_id),
                    'title': data['title'],
                    'description': data['description'],
                    'image': image,
                })
        finally:
            await connection.close()

        self.write(tornado.escape.json_encode({'links': links}))


class LinkHandler(tornado.web.RequestHandler):
    async def get(self, pk, *args, **kwargs):
        connection = await make_connection()
        try:
            link = await connection.fetchrow('SELECT * FROM links WHERE id = $1', int(pk))
        finally:
            await connection.close()

        if link is None:
            raise tornado.web.HTTPError(status_code=404)

        self.write(tornado.escape.json_encode(dict(link)))


def make_app():
    return tornado.web.Application([
        (r'/links', LinksSaverHandler),
        (r'/links/(?P<pk>[0-9]+)$', LinkHandler),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(settings.TORNADO_PORT)
    tornado.ioloop.IOLoop.current().start()
