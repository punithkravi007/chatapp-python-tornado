import logging
import tornado.web
from tornado.options import options

from chat_app.config import settings
from chat_app.handlers import ChatApplicationHandler, ChatApplicationWebSocketHandler
from chat_app.manager import ChatApplicationManager


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        filemode='w',
        filename='app.log',
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    options.parse_command_line()

    chat_app_manager = ChatApplicationManager()

    urls = [
        (r'/$', ChatApplicationHandler),
        (r"/chat/ws$", ChatApplicationWebSocketHandler, dict(app_manager=chat_app_manager))
    ]

    application = tornado.web.Application(
        urls,
        debug=options.debug,
        autoreload=options.debug,
        **settings
    )
    logging.info(f'Chat Application has started on port {options.port} with Debug Mode set to {options.debug}')
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
