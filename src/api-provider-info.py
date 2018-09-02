
class ApiProviderInfo:


    def __init__(self, apiAccessId, apiAccessKey):
        self.__apiAccessId = apiAccessId
        self.__apiAccessKey = apiAccessKey

    def get_apiAcessId(self):
        return self.__apiAccessId