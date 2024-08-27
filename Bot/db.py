from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.server_api import ServerApi
from os import getenv


class DB:
    __instance = None

    def __init__(self):
        if not DB.__instance:
            host = getenv("MONGO_HOST")
            port = getenv("MONGO_PORT")
            self._client = MongoClient(f"mongodb://{host}:{port}", server_api=ServerApi("1"))
            self._users = self._client["bot"]["users"]
        else:
            self = self.getInstance()

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = DB()
        return cls.__instance

    def create_user(self, userid: int) -> bool:
        try:
            if not self._users.find_one({"userid": userid}):
                user = {"userid": userid}
                self._users.insert_one(user)
                return True
        except PyMongoError as ex:
            print(f"Exception while creating user:\n{ex}")
        return False

    def find_by_userid(self, userid: int):
        try:
            user = self._users.find_one({"userid": userid})
            return user
        except PyMongoError as ex:
            print(f"Exception while getting user by userid:\n{ex}")

    def update_user(self, userid: int, **kwargs) -> bool:
        try:
            if self._users.find_one({"userid": userid}) is not None:
                self._users.update_one(
                    {"userid": userid},
                    {"$set": kwargs}
                )
                return True
        except PyMongoError as ex:
            print(f"Exception while updating user:\n{ex}")
        return False



# if __name__ == "__main__":
#     load_dotenv(find_dotenv())
#     db = DB.getInstance()
#     # db.update_user('4876543', 'address', 'Гуруруру')
#     print(db.find_by_userid('4876543'))
