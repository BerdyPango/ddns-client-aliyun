#!/usr/bin/env python
# coding=utf-8
import socket

from utils import DDNSUtils

class DomainSection:
    """
    Object represents dns config section.
    """
    def __init__(self, domainName, subDomainName, type):
        self.domainName = domainName
        self.subDomainName = subDomainName
        self.type = type

    @classmethod
    def from_full_domain(cls, fullDomain, type):
        subDomain = fullDomain.split('.')[0]
        domain = fullDomain.lstrip(subDomain).strip().strip('.')
        record = cls(domain, subDomain, type)
        return record

    def get_dns_resolved_ip(self):
        if self.subDomainName == "@":
            hostname = self.domainName
        else:
            hostname = "{0}.{1}".format(self.subDomainName, self.domainName)
        
        try:
            ip_addr = socket.gethostbyname(hostname)
            DDNSUtils.info("RR value read: [{0}] for [{1}]".format(ip_addr, hostname))
            return ip_addr
        except Exception as exception:
            DDNSUtils.err("Failed to read ip address for [{0}]".format(hostname))
            raise exception
