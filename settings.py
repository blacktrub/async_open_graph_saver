import os

TORNADO_PORT = 8888

POSTGRES = {
    'host': '127.0.0.1',
    'port': 5432,
    'user': 'admin',
    'password': 'admin',
    'database': 'open_graph_links',
}

PROTOCOL = 'http'

HOST = '127.0.0.1'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR_NAME = 'media'
DOWNLOAD_DIR = os.path.join(BASE_DIR, DOWNLOAD_DIR_NAME)
