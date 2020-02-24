'''
    Metadataplus Server

    Elasticsearch 7 is requied as the database server.

    Add the following to the hosts file for testing:
        127.0.0.1 geo.localhost

'''


import tornado.web
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.routing import HostMatches

from handlers import ncbi_geo, immport

define("port", default="8000", help="local port to run the server")
options.parse_command_line()


class PageNotFoundHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.set_status(404)
        self.finish()


def main():

    application = tornado.web.Application([
        (HostMatches(r'geo\..+'), ncbi_geo.NCBIProxyHandler),
        (r"/sitemap.xml", tornado.web.RedirectHandler, {"url": "/static/sitemap.xml"}),
        (r"/(|(?:css|js|img)/.*)", tornado.web.StaticFileHandler,
         dict(path="dist", default_filename="index.html")),
        (r"/geo/(GSE\d+)", ncbi_geo.NCBIGeoDatasetWrapper),
        (r"/geo/_random.html", ncbi_geo.NCBIRandomDatasetExplorer),
        (r"/immport/(SDY\d+)", immport.PlusWrapper),
    ],
        static_path='static',
        default_handler_class=PageNotFoundHandler
    )

    server = tornado.httpserver.HTTPServer(application, xheaders=True)
    server.bind(options.port)
    server.start()

    IOLoop.current().start()


if __name__ == '__main__':
    main()
