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
            self.__X_MIN: int = env_vars["X_MIN"]
            self.__Y_MIN: int = env_vars["Y_MIN"]
            self.__X_MAX: int = env_vars["X_MAX"]
            self.__Y_MAX: int = env_vars["Y_MAX"]
            self.__DEBUG: int = env_vars["DEBUG"]

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
    def X_MIN(cls):
        return cls.get_instance().__X_MIN

    @ClassProperty
    def Y_MIN(cls):
        return cls.get_instance().__Y_MIN

    @ClassProperty
    def X_MAX(cls):
        return cls.get_instance().__X_MAX

    @ClassProperty
    def Y_MAX(cls):
        return cls.get_instance().__Y_MAX

    @ClassProperty
    def DEBUG(cls):
        return cls.get_instance().__DEBUG