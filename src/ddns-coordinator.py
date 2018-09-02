
from utils import DDNSUtils

class DDNSCoordinator(object):

    def __init__(self, config):
        self.config = config
        self.current_records_list = []


    def perform_ddns(self):
        localPublicIp = DDNSUtils.get_current_public_ip()

        if not localPublicIp:
            DDNSUtils.err_and_exit("Failed to get current public IP")