from tornado.web import RequestHandler


class MainHandler(RequestHandler):

    def get(self):
        return self.write({'hello': 'world'})
