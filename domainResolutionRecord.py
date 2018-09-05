#!/usr/bin/env python
# coding=utf-8
import socket

class DomainResolutionRecord:


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
        ip_addr = socket.gethostbyname(hostname)
        return ip_addr

record = DomainResolutionRecord('berdypango.cn','ha','A')
ip_addr = record.get_dns_resolved_ip()
print(ip_addr)