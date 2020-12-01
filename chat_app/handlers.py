import json

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler, WebSocketClosedError

from chat_app.manager import UserAlreadyExistError


class ChatApplicationHandler(RequestHandler):
    def get(self):
        self.render('index.html')


class ChatApplicationWebSocketHandler(WebSocketHandler):

    def initialize(self, app_manager, *args, **kwargs):
        self.app_manager = app_manager
        super().initialize(*args, **kwargs)

    def open(self):
        pass

    def on_close(self):
        print("Connection Closed")
        self.app_manager.de_register_user(self)
        online_users, online_user_handlers = self.app_manager.get_registered_users()
        for handler in online_user_handlers:
            for k, v in handler.items():
                v.send_message(action="registered-users", data=online_users)

    def on_message(self, message):
        try:
            action = json.loads(message)["action"]
            data = json.loads(message)["data"]
            if action == "register-user":
                self.app_manager.register_user(data, self)
                online_users, online_user_handlers = self.app_manager.get_registered_users()
                for handler in online_user_handlers:
                    for k, v in handler.items():
                        v.send_message(action="registered-users", data=online_users)
            elif action == "start_conversation":
                pair = (data["source_user"], data["target_user"])
                conversation_id = self.app_manager.get_conversation_id(pair)
                source_response = {
                    "target_user_id": data["target_user"],
                    "target_user_name": self.app_manager.get_user_name_by_id(data["target_user"]),
                    "target_messages": self.app_manager.get_conversation_by_id(conversation_id)
                }
                self.send_message(action="chat_connected_to_user", data=source_response)
            elif action == "sent_message":
                conversation_id = self.app_manager.add_message_to_conversation(data)
                source_response = {
                    "target_user_id": data["msg_to"],
                    "target_user_name": self.app_manager.get_user_name_by_id(data["msg_to"]),
                    "source_user_id": data["msg_from"],
                    "source_user_name": self.app_manager.get_user_name_by_id(data["msg_from"]),
                    "target_messages": self.app_manager.get_conversation_by_id(conversation_id)
                }
                self.send_message(action="chat_connected_to_user", data=source_response)
                self.send_paired_message(user_id=data["msg_to"], action="message_received", data=source_response)

        except UserAlreadyExistError as ux:
            self.send_message(action="user_already_exist")

    def send_message(self, action=None, data=None):
        message = {
            "action": action,
            "content": data
        }
        try:
            self.write_message(message)
        except WebSocketClosedError:
            self.close()

    def send_paired_message(self, user_id=None, action=None, data=None):
        pair_handler = self.app_manager.get_user_handler(user_id)
        message = {
            "action": action,
            "content": data
        }
        pair_handler.write_message(message)
