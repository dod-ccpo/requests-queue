from requests_queue.handlers.base import BaseHandler


class StatusHandler(BaseHandler):

    def get(self):
        self.write({"status": "ok"})
