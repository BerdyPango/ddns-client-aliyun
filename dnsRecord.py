import sys
import string


def lower_func(s):
    return string.lower(s)

class DnsRecord:
    """
    Object represents dns resolution record.
    """
    def __init__(self, dns_resolution_record):
        self.domainname = None
        self.recordid = None
        self.rr = None
        self.type = None
        self.value = None
        self.ttl = None
        self.priority = None
        self.line = None
        self.status = None
        self.locked = False

        lowered_info = map(lower_func, dns_resolution_record.keys(), dns_resolution_record.values())
        tuples = zip(lowered_info)
        converted_dns_resolution_info = dict(tuples)

        for key in converted_dns_resolution_info.keys():
            self.__dict__[key] = converted_dns_resolution_info[key]
            