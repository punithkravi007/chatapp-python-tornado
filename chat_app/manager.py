class UserAlreadyExistError(Exception):

    def __init__(self, message):
        super().__init__(message)


class ChatApplicationManager(object):
    conversation_identifier = 1

    def __init__(self):
        self._online_users = []
        self._handlers = []
        self._conversation_pairs = {}
        self._conversation = {}

    def register_user(self, user, handler):
        for u in self._online_users:
            if user["user_id"] == u["user_id"]:
                print("User Already Exist")
                raise UserAlreadyExistError("User Already Exist")
        else:
            user_info = dict()
            user_info["user_id"] = user["user_id"]
            user_info["username"] = user["user_name"]
            self._online_users.append(user_info)

            handler_info = dict()
            handler_info[user["user_id"]] = handler
            self._handlers.append(handler_info)
            print("User registered successfully")

    def get_registered_users(self):
        return self._online_users, self._handlers

    def get_user_handler(self, user_id=None):
        for h in self._handlers:
            for k, v in h.items():
                if user_id == k:
                    return v

    def de_register_user(self, handler):
        user_id = None
        for u in self._handlers:
            for k, v in u.items():
                if v == handler:
                    user_id = k
                    break

        for i, u in enumerate(self._online_users):
            if u["user_id"] == user_id:
                self._online_users.pop(i)

    def get_conversation_id(self, pair):
        is_pair_exist = pair in self._conversation_pairs.values() or pair[::-1] in self._conversation_pairs.values()
        print(is_pair_exist)
        conversation_id = None
        if is_pair_exist:
            for k, v in self._conversation_pairs.items():
                if v == pair or v == pair[::-1]:
                    conversation_id = k
                    break
        else:
            temp = ChatApplicationManager.conversation_identifier + 1
            self._conversation_pairs[temp] = pair
            conversation_id = temp
            ChatApplicationManager.conversation_identifier = temp
        return conversation_id

    def get_user_name_by_id(self, user_id):
        for u in self._online_users:
            for k, v in u.items():
                if k == "user_id" and u["user_id"] == user_id:
                    return u["username"]

    def get_conversation_by_id(self, conversation_id):
        if conversation_id in self._conversation.keys():
            return self._conversation[conversation_id]
        else:
            return []

    def add_message_to_conversation(self, message):
        pair = (message["msg_from"], message["msg_to"])
        conversation_id = self.get_conversation_id(pair)
        if conversation_id in self._conversation.keys():
            print("----STEP-2--------")
            self._conversation[conversation_id].append(message)
        else:
            print("------STEP-1----------")
            self._conversation[conversation_id] = [message]
        print(self._conversation)
        return conversation_id






