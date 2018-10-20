import json

from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest, UpdateDomainRecordRequest

from utils import DDNSUtils
from config import Config
from dnsRecord import DnsRecord


class DDNSCoordinator:
    """
    Construct a DDNSCoordinator object with a given Config object

    Args:
        configuration: the given Config object
    """

    def __init__(self, configuration):

        self.configuration = configuration
        self.access_key_id = configuration.apiProviderInfo.access_key_id
        self.access_Key_secret = configuration.apiProviderInfo.access_key_secret
        self.current_records_list = []

    def perform_ddns(self):
        """
        Perform the ddns process when everything is ready
        """
        current_public_ip = DDNSUtils.get_current_public_ip()

        if not current_public_ip:
            DDNSUtils.err_and_exit("Failed to get local public IP")

        DDNSUtils.info(
            "Local public ip address read: [{0}]".format(current_public_ip))

        for record_to_update in self.configuration.recordsToUpdate:
            dns_resolved_ip = record_to_update.get_dns_resolved_ip()

            if current_public_ip == dns_resolved_ip:
                DDNSUtils.info("Skipped as no changes for DomainRecord: [{rec.subDomainName}.{rec.domainName}]".format(
                    rec=record_to_update))
                continue

            # If current public IP doesn't equal to current DNS resolved ip, only in three cases:
            # 1. The new synchronized IP for remote record in api provider doesn't take effect yet
            # 2. remote record's IP in Aliyun server has changed
            # 3. current public IP is changed
            dns_record = self.get_dns_record(record_to_update)
            if not dns_record:
                DDNSUtils.err("Failed to get dns resolution record for [{rec.subDomainName}.{rec.domainName}]".format(
                    rec=record_to_update))
                continue

            if current_public_ip == dns_record.value:
                DDNSUtils.info("Skipped: dns record already updated: [{rec.subDomainName}.{rec.domainName}]".format(
                    rec=record_to_update))
                continue

            dns_record.value = current_public_ip
            result = self.update_dns_record(dns_record, current_public_ip)
            if not result:
                DDNSUtils.err("Failed to update dns record: [{rec.subDomainName}.{rec.domainName}]".format(
                    rec=record_to_update))
            else:
                DDNSUtils.info("Successfully update dns record: [{rec.subDomainName}.{rec.domainName}]".format(
                    rec=record_to_update))

    def get_dns_record(self, dns_section):
        """
        Get the dns record from dns provider by a given dns section
        """
        DDNSUtils.info("Reading dns records for [{section.subDomainName}.{section.domainName}], type=[{section.type}]".format(
            section=dns_section))

        acsClient = AcsClient(
            ak=self.access_key_id, secret=self.access_Key_secret, region_id='cn-hangzhou')
        request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        request.set_DomainName(dns_section.domainName)
        request.set_accept_format('json')
        result = acsClient.do_action_with_exception(request)
        result = json.JSONDecoder().decode(result)

        dns_record_list = result['DomainRecords']['Record']

        if not dns_record_list:
            DDNSUtils.err("Failed to fetch dns resolution records for [{rec.domainName}] by rr={rec.subDomainName} and type={rec.type}".format(
                rec=dns_section))
            return None

        matched_records = []

        for record in dns_record_list:
            if record['DomainName'] == dns_section.domainName and record['RR'] == dns_section.subDomainName and record['Type'] == dns_section.type:
                matched_records.append(record)

        if not matched_records:
            return None

        if len(matched_records) > 1:
            DDNSUtils.err('Duplicate dns resolution records: [{rec.subDomainName}.{rec.domaiNname}]'.format(
                rec=dns_section))

        try:
            dns_record = DnsRecord(matched_records[0])
        except Exception as exception:
            raise exception

        return dns_record

    def update_dns_record(self, dns_record, public_ip):
        """
        Update a dns record at dns provider side with a given dns record
        """
        DDNSUtils.info(
            'Updating value [{rec.value}] for [{rec.rr}.{rec.domainname}]'.format(rec=dns_record))
        acsClient = AcsClient(
            ak=self.access_key_id, secret=self.access_Key_secret, region_id='cn-hangzhou')
        request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        request.set_RR(dns_record.rr)
        request.set_Type(dns_record.type)
        request.set_Value(dns_record.value)
        request.set_RecordId(dns_record.recordid)
        request.set_TTL(dns_record.ttl)
        request.set_accept_format('json')
        try:
            result = acsClient.do_action_with_exception(request)
            return result
        except Exception as exception:
            DDNSUtils.err(
                'Failed to update value [{rec.value}] for [{rec.rr}.{rec.domainname}]'.format(rec=dns_record))
            raise exception
