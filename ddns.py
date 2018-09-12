import sys
import os
import argparse

from utils import DDNSUtils
from config import Config
from ddnsCoordinator import DDNSCoordinator

argParser = argparse.ArgumentParser("DDNS python client")
argParser.add_argument('--domains', '-d', nargs = '*', help = 'The domain name resolution records to be updated.')
argParser.add_argument("--type", '-t', default = 'A', help = 'The resolution type of dns record.')
argParser.add_argument("--access-id", '-i', help = 'The access id used for ddns api provider.')
argParser.add_argument("--access-key", '-k', help = 'The access key used for ddns api provider.')
argParser.add_argument("--config", '-c', help = 'The configuration file to refer to for ddns process. If this option is set, all other options will be ignored.')

args = argParser.parse_args('-i 12314325 -k 123243545 -d www.example.com'.split())

print(args)

if args.config: 
    CONFIG_FILE_PATH = args.config
    if not os.path.exists(CONFIG_FILE_PATH):
        DDNSUtils.err_and_exit('File not found: {0}'.format(CONFIG_FILE_PATH))
    config = Config.from_config_file(CONFIG_FILE_PATH)
    coordinator = DDNSCoordinator(config)
    coordinator.perform_ddns()
    sys.exit()

if not args.domains or not args.access_id or not args.access_key:
    argParser.print_help()
else:
    config = Config.from_cli_options(args.domains, args.access_id, args.access_key, args.type)
    coordinator = DDNSCoordinator(config)
    coordinator.perform_ddns()

sys.exit()
