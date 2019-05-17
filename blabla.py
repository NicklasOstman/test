#! /usr/bin/env python
"""
This script prints the product.yml as json
The json file is cached for 100 seconds (1.6 minutes)
"""
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from anyconfig import load
from json import dumps
from sys import exit, argv
from time import time
from os.path import isfile, join, dirname
from os import remove
from glob import glob

# generate epoch time (seconds -100)
epoch_time = str(int(time()))[:-2]
json_file = '.tmp/product.{epoch}.json'.format(epoch=epoch_time)
json_config = None


def main(arguments):
    parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--force', required=False, default=False, action='store_true', help='overrides the cache')
    parser.add_argument('-q', '--quite', required=False, default=False, action='store_true', help='no output')
    parser.add_argument('-g', '--get', required=False, default=False, nargs=2, help='specific parameter')
    args = parser.parse_args(arguments)

    if args.get:
        import sys
        sys.path.append(join(dirname(__name__), '.'))
        from lib.utils.config import Config
        from lib.utils.aws_profile import AwsProfile
        AwsProfile().set_profile('external')
        print Config().get_config(args.get[0], args.get[1])
        return

    # cache file exist
    if isfile(json_file) and not args.force:
        with open(json_file, 'r') as f:
            json_config = f.read()
    else:
        # clean up old cached files
        for f in glob(".tmp/product*.json"):
            remove(f)

        # create a cache file
        yml_config = load('conf/product.yml')
        json_config = dumps(yml_config)
        with open(json_file, 'w') as f:
            f.write(json_config)

    if not args.quite:
        print json_config


if __name__ == '__main__':
    exit(main(argv[1:]))

