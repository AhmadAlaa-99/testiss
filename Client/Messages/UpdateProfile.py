from Messages import Message as Ms
class UpdateProfile(Ms.Message):
    def __init__(self, phone_number: str,location:str, user_name: str,message: dict = None):
        try:
            if message is None:
                self.message_info = {
                    "Type": "UpdateProfile",
                    "phone_number": phone_number,
                    "location":location,
                    "user_name": user_name,
               
                }
            elif message["Type"] == "UpdateProfile":
                super(UpdateProfile, self).__init__(message=message)
        except Exception as e:
            print(e)
