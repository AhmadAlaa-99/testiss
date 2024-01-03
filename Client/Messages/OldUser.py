from Messages import Message as Ms


class OldUserMessage(Ms.Message):
    def __init__(self, user_name: str, password: str, public_key: str,national_number: str,message: dict = None):
        try:
            if message is None:
                self.message_info = {
                    "Type": "OldUser",
                    "user_name": user_name,
                    "password": password,
                    "public_key": public_key,
                    "national_number":national_number,
                }
            elif message['Type'] == "OldUser":
                super(OldUserMessage, self).__init__(message=message)
        except Exception as e:
            print(e)
