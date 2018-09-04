import configparser as ConfigParser

from utils import DDNSUtils
from apiProviderInfo import ApiProviderInfo
from domainnameRecord import DomainNameRecord

class Config:
    """
    The object that holds the configuration to perform ddns
    """
    def __init__(self, apiProviderInfo, interval, recordsToUpdate):
        self.apiProviderInfo = apiProviderInfo
        self.interval = interval
        self.recordsToUpdate = recordsToUpdate

    @classmethod
    def fromConfigFile(cls, configFilePath):
        parser = ConfigParser.ConfigParser()
        if not parser.read(configFilePath):
            DDNSUtils.err_and_exit("Failed to read config file.")

        try:
            interval = parser.get("DEFAULT", "interval")
            if not interval:
                DDNSUtils.err_and_exit("Invalid interval in config file.")

            access_id = parser.get("ApiProvider", "access_id")
            access_key = parser.get("ApiProvider", "access_key")
            if not access_id or not access_key:
                DDNSUtils.err_and_exit("Invalid access_id or access_key in config file.")
            apiProviderInfo = ApiProviderInfo(access_id,access_key)

            recordsSections = [s for s in parser.sections() if s.startswith("DomainNameToUpdate") ]
            records = []

            for record in recordsSections:
                domain = parser.get(record,'domain')
                type = parser.get(record,'type')
                subDomains = parser.get(record,'sub_domain').split(',')
                if not domain or not type or not subDomains:
                    DDNSUtils.err_and_exit("Invalid domian record.")

                for subDomain in subDomains:
                    record = DomainNameRecord(domain, subDomain.strip(), type)
                    records.append(record)
            config = Config(apiProviderInfo, interval, records)
            return config

        except ValueError as ex:
            DDNSUtils.err_and_exit("Invalid debug in config: {0}".format(ex))
        except ConfigParser.NoSectionError as ex:
            DDNSUtils.err_and_exit("Invalid config: {0}".format(ex))
        except ConfigParser.NoOptionError as ex:
            DDNSUtils.err_and_exit("Invalid config: {0}".format(ex))

try:
    import os
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../ddns.conf.sample')
    config = Config.fromConfigFile(filename)
    assert config.interval == '500'
    assert config.apiProviderInfo.apiAccessId == '1234567890'
    assert config.apiProviderInfo.apiAccessKey == '0987654321'
except Exception as error:
    print("error: {0}".format(error.args))
else:
    pass