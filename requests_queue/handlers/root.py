from requests_queue.handlers.base import BaseHandler


class RootHandler(BaseHandler):

    def get(self):
        self.write("Hello from requests-queue")
