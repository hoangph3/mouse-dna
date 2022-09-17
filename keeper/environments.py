import json
from . import ClassProperty


class SystemEnv:
    __instance: dict = None

    @staticmethod
    def get_instance():
        if not SystemEnv.__instance:
            return SystemEnv()

        return SystemEnv.__instance

    def __init__(self) -> None:
        if SystemEnv.__instance:
            raise Exception("This class cannot initialize")
        else:
            SystemEnv.__instance = self

            with open("./env.json") as f:
                env_vars = json.load(f)

            self.__EXPIRATION_ACTION_TIME: str = env_vars["EXPIRATION_ACTION_TIME"]
            self.__MIN_ACTION_LENGTH: str = env_vars["MIN_ACTION_LENGTH"]
            self.__CURVE_THRESHOLD: int = env_vars["CURVE_THRESHOLD"]
            self.__MM_CODE: str = env_vars["MM_CODE"]
            self.__PC_CODE: str = env_vars["PC_CODE"]
            self.__DD_CODE: int = env_vars["DD_CODE"]
            self.__X_LIMIT: int = env_vars["X_LIMIT"]
            self.__Y_LIMIT: int = env_vars["Y_LIMIT"]

    @ClassProperty
    def EXPIRATION_ACTION_TIME(cls):
        return cls.get_instance().__EXPIRATION_ACTION_TIME

    @ClassProperty
    def MIN_ACTION_LENGTH(cls):
        return cls.get_instance().__MIN_ACTION_LENGTH

    @ClassProperty
    def CURVE_THRESHOLD(cls):
        return cls.get_instance().__CURVE_THRESHOLD

    @ClassProperty
    def MM_CODE(cls):
        return cls.get_instance().__MM_CODE

    @ClassProperty
    def PC_CODE(cls):
        return cls.get_instance().__PC_CODE

    @ClassProperty
    def DD_CODE(cls):
        return cls.get_instance().__DD_CODE

    @ClassProperty
    def X_LIMIT(cls):
        return cls.get_instance().__X_LIMIT

    @ClassProperty
    def Y_LIMIT(cls):
        return cls.get_instance().__Y_LIMIT
