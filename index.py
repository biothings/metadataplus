'''
    Metadataplus Server

    Elasticsearch 7 is requied as the database server.

    Add the following to the hosts file for testing:
        127.0.0.1 immport.localhost
        127.0.0.1 geo.localhost

    Run with --host=localhost

'''


import tornado.web
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.routing import HostMatches

from handlers import ncbi_geo, immport

define("host", default="metadataplus.biothings.io", help="server hostname")
define("port", default="8000", help="local port to run the server")
options.parse_command_line()


class PageNotFoundHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.set_status(404)
        # self.render("dist/404.html", redirect_url="/geo/_random.html?redirect")


def main():

    application = tornado.web.Application([
        (HostMatches('geo.' + options.host), ncbi_geo.NCBIProxyHandler),
        (HostMatches('immport.' + options.host), immport.ImmPortProxyHandler),
        (r"/sitemap.xml", tornado.web.RedirectHandler, {"url": "/static/sitemap.xml"}),
        (r"/(|(?:css|js|img)/.*)", tornado.web.StaticFileHandler,
         dict(path="dist", default_filename="index.html")),
        (r"/geo/(GSE\d+)", ncbi_geo.NCBIGeoDatasetWrapper),
        (r"/geo/_random.html", ncbi_geo.NCBIRandomDatasetExplorer),
        (r"/immport/(SDY\d+)", immport.ImmPortDatasetWrapper),
    ],
        xheaders=True,
        static_path='static',
        default_handler_class=PageNotFoundHandler
    )

    server = tornado.httpserver.HTTPServer(application)
    server.bind(options.port)
    server.start()

    IOLoop.current().start()


if __name__ == '__main__':
    main()
