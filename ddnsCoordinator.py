
from utils import DDNSUtils
from config import Config

class DDNSCoordinator:
    """
    An object to coordinate the ddns process
    """

    def __init__(self, configuration):
        self.configuration = configuration
        self.current_records_list = []


    def perform_ddns(self):
        current_public_ip = DDNSUtils.get_current_public_ip()

        if not current_public_ip:
            DDNSUtils.err_and_exit("Failed to get current public IP")

        for record_to_update in self.configuration.recordsToUpdate:
            dns_resolved_ip = record_to_update.get_dns_resolved_ip()

            if current_public_ip == dns_resolved_ip:
                DDNSUtils.info("Skipped as no changes for DomainRecord" \
                           "[{rec.subDomainName}.{rec.domainName}]".format(rec=record_to_update))
            continue

        # If current public IP doesn't equal to current DNS resolved ip, only in three cases:
        # 1. The new synchronized IP for remote record in api provider doesn't take effect yet
        # 2. remote record's IP in Aliyun server has changed
        # 3. current public IP is changed

