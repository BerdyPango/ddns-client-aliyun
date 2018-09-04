
class ApiProviderInfo:
    """
    An object holds the information for api provider
    """

    def __init__(self, apiAccessId, apiAccessKey):
        self.apiAccessId = apiAccessId
        self.apiAccessKey = apiAccessKey

    def get_apiAcessId(self):
        return self.apiAccessId