
from utils import DDNSUtils
from config import Config

class DDNSCoordinator:
    """
    An object to coordinate the ddns process
    """

    def __init__(self, Config):
        self.configuration = Config
        self.current_records_list = []


    def perform_ddns(self):
        localPublicIp = DDNSUtils.get_current_public_ip()

        if not localPublicIp:
            DDNSUtils.err_and_exit("Failed to get current public IP")