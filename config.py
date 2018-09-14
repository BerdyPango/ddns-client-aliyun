import configparser as ConfigParser

from utils import DDNSUtils
from apiProviderInfo import ApiProviderInfo
from domainSection import DomainSection

class Config:
    """
    The object that holds the configuration to perform ddns

    Args:
        apiProviderInfo: the object holds the api provider information
        recordsToUpdate: a list holding all the domain name resolution records to update
    Returns: 
        An object of Config
    """
    def __init__(self, apiProviderInfo, recordsToUpdate):
        self.apiProviderInfo = apiProviderInfo
        self.recordsToUpdate = recordsToUpdate

    @classmethod
    def from_config_file(cls, configFilePath):
        """
        Construct a Config object from a given config file path

        Args:
            configFilePath: path of the given config file
        Returns: 
            An object of Config
        """
        parser = ConfigParser.ConfigParser()
        if not parser.read(configFilePath):
            DDNSUtils.err_and_exit("Failed to read config file.")

        try:
            access_id = parser.get("ApiProvider", "access_id")
            access_key = parser.get("ApiProvider", "access_key")
            
            if not access_id or not access_key:
                DDNSUtils.err_and_exit("Invalid access_id or access_key in config file.")
            apiProviderInfo = ApiProviderInfo(access_id,access_key)

            DDNSUtils.info("Read Access Id: {0}".format(access_id))
            DDNSUtils.info("Read Access Key: {0}".format(access_key))

            recordsSections = [s for s in parser.sections() if s.startswith("DomainNameToUpdate") ]

            records = []
            for record in recordsSections:
                domain = parser.get(record,'domain')
                type = parser.get(record,'type')
                subDomains = parser.get(record,'sub_domain').split(',')
                if not domain or not type or not subDomains:
                    DDNSUtils.err_and_exit("Invalid domian record.")
                
                DDNSUtils.info("Read Domain: {0}".format(domain))
                DDNSUtils.info("Read Sub Domains: {0}".format(subDomains))
                DDNSUtils.info("Read Type: {0}".format(type))

                for subDomain in subDomains:
                    record = DomainSection(domain, subDomain.strip(), type)
                    records.append(record)
            config = cls(apiProviderInfo, records)
            return config

        except ValueError as ex:
            DDNSUtils.err_and_exit("Invalid debug in config: {0}".format(ex))
        except ConfigParser.NoSectionError as ex:
            DDNSUtils.err_and_exit("Invalid config: {0}".format(ex))
        except ConfigParser.NoOptionError as ex:
            DDNSUtils.err_and_exit("Invalid config: {0}".format(ex))

    @classmethod
    def from_cli_options(cls, domains, access_id, access_key, type):
        if not domains or not access_id or not access_key:
            DDNSUtils.err_and_exit("Aruguments are not sufficient.")
        
        apiProviderInfo = ApiProviderInfo(access_id, access_key)

        records = []
        try:
            for fullDomain in domains:
                record = DomainSection.from_full_domain(fullDomain, type)
                records.append(record)
            config = cls(apiProviderInfo, records)
            return config
        except ValueError as ex:
            DDNSUtils.err_and_exit("Invalid parameters in config: {0}".format(ex))

try:
    import os
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'config-samples/ddns.conf.sample')
    config = Config.from_config_file(filename)
    assert config.apiProviderInfo.apiAccessId == '1234567890'
    assert config.apiProviderInfo.apiAccessKey == '0987654321'

    config = Config.from_cli_options(['www.example.com','api.example.com'],'123435454','123243545','A')
    assert config.apiProviderInfo.apiAccessId == '123435454'
    assert config.apiProviderInfo.apiAccessKey == '123243545'
except Exception as error:
    print("error: {0}".format(error.args))
else:
    pass