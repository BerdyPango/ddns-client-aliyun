from configparser import ConfigParser
from configparser import NoSectionError
from configparser import NoOptionError

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
        Instance of Config
    """
    def __init__(self, apiProviderInfo, recordsToUpdate):
        self.apiProviderInfo = apiProviderInfo
        self.recordsToUpdate = recordsToUpdate

    @classmethod
    def from_config_file(cls, configFilePath):
        """
        Construct a Config object from a given config file

        Args:
            configFilePath: path to the given config file
        Returns: 
            Instance of Config
        """
        parser = ConfigParser()
        if not parser.read(configFilePath):
            DDNSUtils.err_and_exit("Failed to read config file.")

        try:
            access_key_id = parser.get("ApiProvider", "access_key_id")
            access_key_secret = parser.get("ApiProvider", "access_key_secret")
            
            if not access_key_id or not access_key_secret:
                DDNSUtils.err_and_exit("Invalid access_id or access_key in config file.")
            apiProviderInfo = ApiProviderInfo(access_key_id, access_key_secret)

            DDNSUtils.info("Read Access Key Id: [{0}]".format(access_key_id))
            DDNSUtils.info("Read Access Key Secret: [{0}]".format(access_key_secret))

            recordsSections = [s for s in parser.sections() if s.startswith("DomainNameToUpdate") ]

            records = []
            for record in recordsSections:
                domain = parser.get(record,'domain')
                type = parser.get(record,'type')
                subDomains = parser.get(record,'sub_domain').split(',')
                if not domain or not type or not subDomains:
                    DDNSUtils.err_and_exit("Invalid domian record.")
                
                DDNSUtils.info("Read Domain: [{0}]".format(domain))
                DDNSUtils.info("Read Sub Domains: [{0}]".format(subDomains))
                DDNSUtils.info("Read Type: [{0}]".format(type))

                for subDomain in subDomains:
                    record = DomainSection(domain, subDomain.strip(), type)
                    records.append(record)
            config = cls(apiProviderInfo, records)
            return config

        except ValueError as ex:
            DDNSUtils.err_and_exit("Invalid debug in config: {0}".format(ex))
        except NoSectionError as ex:
            DDNSUtils.err_and_exit("Invalid config: {0}".format(ex))
        except NoOptionError as ex:
            DDNSUtils.err_and_exit("Invalid config: {0}".format(ex))

    @classmethod
    def from_cli_options(cls, domains, access_key_id, access_key_secret, type):
        """
        Construct a Config object from a set of given configurations

        Args:
            domains: domains to update
            access_key_id: access key id provided by api provider
            access_key_secret: access key secret provided by api provider
            type: dns record type, for now only 'A' is supported
        Returns: 
            Instance of Config
        """
        if not domains or not access_key_id or not access_key_secret:
            DDNSUtils.err_and_exit("Aruguments are not sufficient: domains, access_key_id and access_key_secret")
        
        apiProviderInfo = ApiProviderInfo(access_key_id, access_key_secret)

        records = []
        try:
            for fullDomain in domains:
                record = DomainSection.from_full_domain(fullDomain, type)
                records.append(record)
            config = cls(apiProviderInfo, records)
            return config
        except ValueError as ex:
            DDNSUtils.err_and_exit("Invalid parameters in config: {0}".format(ex))
