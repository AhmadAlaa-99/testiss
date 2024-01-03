import pymongo


class DB:
    def __init__(self, database_name='University_Client'):
        __connection_db = pymongo.MongoClient()
        self.__DB = __connection_db[database_name]

    def get_db_name(self):
        return self.__DB.name

    def insert_new_user(self, user_name: str,role_name:str,national_number:str,public_key:str):
        users = self.__DB['Users'].find({'user_name': user_name})
        if users.count() != 0:
            for user in users:
                #st2 
                #st3 user['PublicKey'] == public_key  
                if user['PublicKey'] == public_key or user['user_name'] == user_name:
                #if  user['user_name'] == user_name : 
                    return -1
        self.__DB['Users'].insert_one({
             'user_name': user_name,
             'role_name': role_name,
             'national_number':national_number,
             #st2
             'PublicKey': public_key,
             #st3
          #  'PublicKey': public_key,
           # 'PrivateKey': private_key
        })

    def insert_new_subject(self, subject_name: str):
        subjects = self.__DB['Subjects'].find({'subject_name': subject_name})
        if subjects.count() != 0:
            for subject in subjects:
                if  subject['subject_name'] == subject_name:
                    return -1
        self.__DB['Subjects'].insert_one({
            'subject_name': subject_name,
        })

    def query(self, collection_name, query):
        return self.__DB[collection_name].find(query)

    def get_users_name(self):
       return [user['user_name'] for user in self.query('Users', {})]

    def names_of_doctors(self):
        return [user['user_name'] for user in self.query('Users', {'role_name': 'doctor'})]
    def names_of_doctor_students(self):
        return [user['user_name'] for user in self.query('Users', {'role_name': 'student'})]
    def names_of_subjects(self):
        return [subject['subject_name'] for subject in self.query('Subjects', {})]
    def get_user_national_number(self, user_name):
        result = self.query("Users", {"user_name": user_name})
        if result and len(result) > 0:
          return result[0]["national_number"]
        else:
          # يمكنك التعامل مع الحالة التي لا يوجد فيها مستخدم بهذا الاسم
         print("لم يتم العثور على المستخدم")
         return None

      

    def get_public_key(self, username):
        res = self.query('Users', {
            'username': username
        })
        return res[0]['PublicKey']

    def get_private_key(self, username):
        res = self.query('Users', {
            'username': username
        })
        return res[0]['PrivateKey']
