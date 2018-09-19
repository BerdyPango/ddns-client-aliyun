#!/usr/bin/env python
# coding=utf-8
"""
 Copyright (C) 2010-2013, Ryan Fan <reg_info@126.com>

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Library General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
"""
import sys
import requests

from datetime import datetime




class DDNSUtils(object):
    
    @staticmethod
    def get_current_public_ip():
        """
        Get current public IP

        @return  IP address or None
        """
        try:
            response = requests.get("http://members.3322.org/dyndns/getip")
        except requests.RequestException as ex:
            msg = "network problem: {0}".format(ex)
            DDNSUtils.err(msg)
            return None

        if response.status_code != requests.codes['ok']:
            msg = "Failed to get current public IP: {0}\n{1}".format(response.status_code, response.content)
            DDNSUtils.err(msg)
            return None

        return response.content.decode('utf-8').rstrip("\n")

    @staticmethod
    def info(msg):
        """
        Output informative message
        :param msg: Message to display
        """
        sys.stdout.write("{0}\t[INFO]\t{1}\n".format(DDNSUtils.get_current_time(), msg))

    @staticmethod
    def err(msg):
        """
        Output error message
        :param msg: Message to display
        """
        sys.stderr.write("{0}\t[ERROR]\t{1}\n".format(DDNSUtils.get_current_time(), msg))

    @staticmethod
    def err_and_exit(msg):
        """
        Output error message and exit
        :param msg: Message to display
        """
        sys.stderr.write("{0}\t[ERROR]\t{1}\n".format(DDNSUtils.get_current_time(), msg))
        sys.exit(1)

    @staticmethod
    def get_current_time():
        """
        Get human readable standard timestamp

        :return: timestamp string
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")