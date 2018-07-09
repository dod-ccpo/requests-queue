from requests_queue.handlers.base import BaseHandler


class RootHandler(BaseHandler):

    def get(self):
        self.set_header('Content-Type', 'text/plain')
        self.write("Hello from requests-queue")
