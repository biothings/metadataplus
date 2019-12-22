'''
    Metadataplus Server

    Elasticsearch 7 is requied as the database server.
    For local testing, set hostname "localtest" to 127.0.0.1 in the os host file.

'''

import tornado.ioloop
import tornado.web
from biothings.web.settings import BiothingESWebSettings
from tornado.options import define, options
from tornado.routing import HostMatches

from api import ncbi_geo

define("geo_resource_host", default="localtest:8000", help="hostname for NCBI GEO resource proxy")
define("server_host", default="localhost:8000", help="hostname for the main app server")
options.parse_command_line()


class PageNotFoundHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.set_status(404)
        self.render("dist/404.html", redirect_url="/geo/_random.html?redirect")


WEB_LIST = [
    (HostMatches(options.geo_resource_host.split(':')[0]), ncbi_geo.NCBIProxyHandler),
    (r"/(|(?:css|js|img)/.*)", tornado.web.StaticFileHandler,
     dict(path="dist", default_filename="index.html")),
    (r"/geo/(GSE\d+)", ncbi_geo.NCBIGeoDatasetWrapper),
    (r"/geo/_random.html", ncbi_geo.NCBIRandomDatasetExplorer),
    (r"/geo/(sitemap\d?.xml)", tornado.web.StaticFileHandler, dict(path="api")),
]

API_SETTINGS = BiothingESWebSettings(config='api.config')

APP_LIST = API_SETTINGS.generate_app_list() + WEB_LIST

if __name__ == '__main__':
    application = tornado.web.Application(
        APP_LIST,
        xheaders=True,
        static_path='dist',
        default_handler_class=PageNotFoundHandler)
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()
