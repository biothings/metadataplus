'''
    Metadataplus Server

    Elasticsearch 7 is requied as the database server.
    For local testing, run application with parameter
        --geo-host=<hostname:port> --server-host=localhost:<port>,
    And set <hostname> to 127.0.0.1 in the os host file.

'''

from sys import platform

import tornado.web
from biothings.web.settings import BiothingESWebSettings
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.routing import HostMatches

from api import ncbi_geo

define("geo_host", default="geo.metadataplus.biothings.io", help="GEO resource proxy hostname")
define("server_host", default="metadataplus.biothings.io", help="Allowed CORS origin hostname")
define("port", default="8000", help="local port to run the server")
options.parse_command_line()


class PageNotFoundHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.set_status(404)
        # self.render("dist/404.html", redirect_url="/geo/_random.html?redirect")


WEB_LIST = [
    (HostMatches(options.geo_host.split(':')[0]), ncbi_geo.NCBIProxyHandler),
    (r"/(|(?:css|js|img)/.*)", tornado.web.StaticFileHandler,
     dict(path="dist", default_filename="index.html")),
    (r"/geo/(GSE\d+)", ncbi_geo.NCBIGeoDatasetWrapper),
    (r"/geo/_random.html", ncbi_geo.NCBIRandomDatasetExplorer),
    (r"/geo/(sitemap\d?.xml)", tornado.web.StaticFileHandler, dict(path="api")),
]

API_SETTINGS = BiothingESWebSettings(config='api.config')

APP_LIST = API_SETTINGS.generate_app_list() + WEB_LIST


def main():

    application = tornado.web.Application(
        APP_LIST,
        xheaders=True,
        static_path='dist',
        default_handler_class=PageNotFoundHandler)

    server = tornado.httpserver.HTTPServer(application)
    server.bind(options.port)
    server.start()

    IOLoop.current().start()


if __name__ == '__main__':
    main()
