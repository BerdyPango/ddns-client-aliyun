


from utils import DDNSUtils
from config import Config
from aliyunResolver import AliYunResolver
from dnsRecord import DnsRecord

class DDNSCoordinator:
    """
    An object to coordinate the ddns process
    """

    def __init__(self, configuration):
        self.configuration = configuration
        self.dnsResolver = AliYunResolver(configuration.access_id,configuration.access_key, True)
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
            dns_record = self.get_dns_record(record_to_update)
            if not dns_record:
                DDNSUtils.err("Failed to get dns resolution record for [{rec.subDomainName}.{rec.DomainName}]".format(rec=record_to_update))
                continue
            
            if current_public_ip == dns_record.value:
                DDNSUtils.info("Skipped: dns record already updated: [{rec.subDomainName}.{rec.DomainName}]".format(rec=record_to_update))
                continue
            
            result = self.update_dns_record(dns_record, current_public_ip)
            if not result:
                DDNSUtils.err("Failed to update dns record: [{rec.subDomainName}.{rec.DomainName}]".format(rec=record_to_update))
            else:
                DDNSUtils.info("Successfully update dns record: [{rec.subDomainName}.{rec.DomainName}]".format(rec=record_to_update))

    def get_dns_record(self, dns_section):

            dns_record_list = self.dnsResolver.get_domain_records(dns_section.domainName, 
                                                                rr_keyword=dns_section.subDomainName, 
                                                                type_keyword=dns_section.type)

            if not dns_record_list:
                DDNSUtils.err("Failed to fetch dns resolution records for {rec.domainName} by rr={rec.subDomainName} and type={rec.type}").format(rec=dns_section)
                return None

            keys_to_check = ('DomainName', 'RR', 'Type')
            matched_records = []

            for record in dns_record_list:
                if all(record.get(key, None) == getattr(dns_section, key.lower()) for key in keys_to_check):
                    matched_records.append(record)

            if not matched_records:
                return None

            if len(matched_records) > 1:
                DDNSUtils.err('Duplicate dns resolution records: {rec.subDomainName}.{rec.domaiNname}').format(rec=dns_section)
            
            try:
                dns_record = DnsRecord(matched_records[0])
            except Exception as exception:
                raise exception
            
            return dns_record

    def update_dns_record(self, dns_record, public_ip):
        return self.dnsResolver.update_domain_record(dns_record.recordid, rr=dns_record.rr, record_value=public_ip)