#!/usr/bin/env python
#!-*- coding:utf-8 -*-

import os
import simplejson as json

import tornado.ioloop
import tornado.web
from tornado.escape import xhtml_escape

TEMPLATE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "./templates")
);

STATIC_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "./static")
);

request_hnd = tornado.web.RequestHandler

marker_num = 2
markers = [
  {'uid':'m1', 'lng':121.481912, 'lat':31.240308},
  {'uid':'m2', 'lng':121.484700, 'lat':31.240308},
]

def db_get_markers():
    global marker_num, markers
    return markers

def db_add_markers(lng, lat):
    global marker_num, markers
    marker_num += 1
    markers.append({'uid':"m"+str(marker_num), 'lng':lng, 'lat':lat})
    print markers

def get_template(tf):
    return os.path.join(TEMPLATE_DIR, tf)

class HomeHandler(request_hnd):
    def get(self):
        return self.render(get_template('home.html'))

class MarkersGetHandler(request_hnd):
    def post(self):
        res = db_get_markers()
        self.write(json.dumps(res))

class MarkersAddHandler(request_hnd):
    def post(self):
        lng = xhtml_escape(self.request.arguments['lng'][0])
        lat = xhtml_escape(self.request.arguments['lat'][0])
        print "lng, lat = ", lng, lat
        db_add_markers(lng, lat)
        self.write(json.dumps('ok'))


settings = {
    "cookie_secret":"7nnezKXQAGwe3uqKKKkL5gEmadfkh7EQnpasdUUU/Vo=",
    "static_path":STATIC_DIR,
    "xsrf_cookies":True,
}

application = tornado.web.Application([
    (r"/", HomeHandler),
    (r"/getmarkers", MarkersGetHandler),
    (r"/addmarkers", MarkersAddHandler),
], **settings)


if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
