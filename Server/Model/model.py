import pymongo


class DB:
    def __init__(self, data_base_name="UniversityServer"):
        __connection_db = pymongo.MongoClient()
        self.__DB = __connection_db[data_base_name]

    def get_db_name(self):
        return self.__DB.name + "DB"

    def insert_new_user(
        self,
        user_name: str,
        password: str,
        role_name: str,
        national_number: str,
        # st3
        public_key: str,
    ):
        user_count = self.__DB["Users"].count_documents({"user_name": user_name})
        if user_count != 0:
            return -1

        self.__DB["Users"].insert_one(
            {
                "user_name": user_name,
                "password": password,
                "role_name": role_name,
                "national_number": national_number,
                # st3
                 "public_key": public_key
                # st3
            }
        )
        return 1

    def query(self, collection_name, query):
        return self.__DB[collection_name].find(query)

    def check_user(self, user_name,public_key):
        q_res = self.query(
            "Users",
            {
                "public_key": public_key,
                "user_name": user_name,
            },
        )
        user_list = list(q_res)  # Convert cursor to list
        user_exists = len(user_list) == 1  # Check if exactly one user is found
        return [user_list[0] if user_exists else None, user_exists]

    def add_active_user(self, user_name, peer,public_key):
        if not self.is_user_active(user_name):
            self.__DB["ActiveUsers"].insert_one(
                {
                    "user_name": user_name,
                    "Peer": peer,
                    "public_key": public_key,
                }
            )

    def remove_active_user(self, user_name, public_key):
        if self.is_user_active(user_name):
            self.__DB["ActiveUsers"].delete_one(
                {"user_name": user_name, "PublicKey": public_key}
            )

    def is_user_active(self, user_name):
        return self.__DB["ActiveUsers"].count_documents({"user_name": user_name}) == 1
    
    def get_user_by_peer(self, peer):
        return self.query("ActiveUsers", {"Peer": peer})

    def add_profile(self, user_name, phone_number, location):
        result = self.__DB["Profile"].update_one(
            {"user_name": user_name},
            {
                "$set": {
                    "phone_number": phone_number,
                    "location": location,
                }
            },
            upsert=True,
        )
        if result.matched_count > 0 or result.upserted_id is not None:
            return 1
        else:
            return -1

    def add_project(self, doctor_name, student_name, subject_name, project_link, file):

        self.__DB["Projects"].insert_one(
            {
                "doctor_name": doctor_name,
                "student_name": student_name,
                "subject_name": subject_name,
                "project_link": project_link,
                "file": file,
            }
        )
        return 1

    def add_mark(self, doctor_name, subject_name, file):
        self.__DB["Marks"].insert_one(
            {
                "doctor_name": doctor_name,
                "subject_name": subject_name,
                "file": file,
            }
        )
        return 1

    def names_of_doctor_students(self, student_name):
        return self.query("Projects", {"student_name": student_name})

    def get_user_elements(self, name):
        return self.query("Elements", {"Name": name})

    def get_element_by_title(self, name, title):
        if self.is_user_active(name):
            res = self.query("Elements", {"Name": name, "Title": title})
        return res

    def update_element(self, name, old_title, title, password, description, files):
        res = self.get_element_by_title(name, old_title)
        if res is None or res.count() == 0:
            return -1
        else:
            self.__DB["Elements"].update_many(
                {"Name": name, "Title": old_title},
                {
                    "$set": {
                        "Title": title,
                        "Name": name,
                        "Password": password,
                        "Description": description,
                        "Files": files,
                    }
                },
            )
            return 1

    def delete_element(self, name, title):
        res = self.get_element_by_title(name, title)
        if res is None or res.count() == 0:
            return -1
        else:
            self.__DB["Elements"].delete_many({"Name": name, "Title": title})
            return 1

    def get_user_national_number(self, user_name):
        res = self.is_user_active(user_name)
        if res == 1:
            return self.query("Users", {"user_name": user_name})[0]["national_number"]
        else:
            return -1

    def get_marks(self, subject_name):
        return self.query("Marks", {"subject_name": subject_name})

    def add_event(self, dic: dict):
        temp = {"Time": datetime.datetime.now().__str__()}
        for key, val in dic.items():
            temp[key] = val
        pubkey = self.get_user_publicKey(dic["Name"])
        temp["PublicKey"] = pubkey
        self.__DB["Events"].insert_one(temp)

    def get_projects(self, student_name):
        return self.query("Projects", {"student_name": student_name})

    def get_user_publicKey(self, user_name):
        res = self.query("Users", {"Name": user_name})
        return res[0]["PublicKey"] if res.count() == 1 else None

    def get_profile(self, user_name):
        return self.query("Profile", {"user_name": user_name})
