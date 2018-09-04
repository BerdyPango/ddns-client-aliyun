import os

from ddnsCoordinator import DDNSCoordinator
from config import Config
from utils import DDNSUtils


def main():
    CONFIG_FILE_PATH = "config/ddns.conf"

    if not os.path.exists(CONFIG_FILE_PATH):
        DDNSUtils.err_and_exit('File not found: {0}'.format(CONFIG_FILE_PATH))

    config = Config.fromConfigFile(CONFIG_FILE_PATH)

    coordinator = DDNSCoordinator(config)
    

    if __name__ == '__main__':
        main()