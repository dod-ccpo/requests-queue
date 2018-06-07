#!/usr/bin/env python

import tornado.ioloop

from requests_queue.make_app import make_app, make_config

app = make_app(make_config())
port = 8888
app.listen(port)
print("Listening on http://localhost:%i" % port)
tornado.ioloop.IOLoop.current().start()
