#!/usr/bin/env python

import tornado.ioloop

from requests_queue.make_app import make_app, make_config

config = make_config()
app = make_app(config)

if __name__ == '__main__':
    port = int(config['default']['port'])
    app.listen(port)
    print("Listening on http://localhost:%i" % port)
    tornado.ioloop.IOLoop.current().start()
