
class Config:
    
    
    def __init__(self, apiProviderInfo, interval, recordsToUpdate):
        self.__apiProviderInfo = apiProviderInfo
        self.__interval = interval
        self.__recordsToUpdate = recordsToUpdate

    def get_apiProviderInfo(self):
        return self.__apiProviderInfo