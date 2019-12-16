import tornado.ioloop
import tornado.web

import logging
import os

log = logging.getLogger("metadataplus")
staticpath = os.path.join(os.path.dirname(__file__), 'dist')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("dist/index.html")

settings={
    "autoreload": True
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/((?:css|js|img)/.*)", tornado.web.StaticFileHandler, {"path": staticpath}),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
