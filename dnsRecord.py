import sys


def lower_func(s):
    return s.lower()

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

        lowered_info = list(map(lower_func, list(dns_resolution_record.keys())))
        tuples = list(zip(lowered_info, list(dns_resolution_record.values())))
        converted_dns_resolution_info = dict(tuples)

        for key in list(converted_dns_resolution_info.keys()):
            self.__dict__[key] = converted_dns_resolution_info[key]
            