import os

from tornado.options import options

options.define("port", default=8080, help="Port to run the server")
options.define("debug", default=True, help="Debug is True")

CHAT_APP_ROOT = os.path.dirname(os.path.realpath(__file__))

settings = {
    "template_path": os.path.join(CHAT_APP_ROOT, "templates"),
    "static_path": os.path.join(CHAT_APP_ROOT, "static")
}
