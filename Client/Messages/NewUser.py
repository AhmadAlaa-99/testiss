import random
from Messages import Message as Ms
import time
import uuid
class NewUser(Ms.Message):
    def __init__(self, user_name: str, password: str,role_name: str,national_number: str,
     public_key: str = None,
     message: dict = None):
        try:
            if message is None:
                self.message_info = {
                    "Type": "NewUser",
                    "user_name": user_name,
                    "password": password,
                    "role_name": role_name,
                    "national_number": national_number,
                    "public_key": public_key if public_key is not None else
                     str(random.randint(0, time.time_ns())) +
                     str(uuid.getnode()) +
                     str(random.randint(0, time.time_ns()))
                }
            elif message['Type'] == 'NewUser':
                super(NewUser, self).__init__(message)
        except Exception as e:
            print(e)