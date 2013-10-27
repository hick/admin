import os

def application(environ, start_response):
  start_response('200 OK', [('Content-Type', 'text/plain')])
  hickvar = "I am Hick"
  hickvar = os.sys.version
  return ["basic passenger for django!!! %s\n" % hickvar]


