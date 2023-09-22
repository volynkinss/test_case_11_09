class MsgData:
    def __init__(self, message):
        self.chat_id = message.chat.id
        self.user_id = message.from_user.id
        self.username = message.from_user.username
        self.name = message.from_user.first_name
        self.surname = message.from_user.last_name
        self.text = message.text
        self.message_id = message.message_id
        self.user_choise = message.web_app_data.data
