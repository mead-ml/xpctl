#!/usr/bin/env python3

import connexion
import logging
import argparse
import os
from xpctl.backends.core import ExperimentRepo
from baseline.utils import read_config_file

from xpctl.xpserver import encoder


def get_logging_level(ll):
    ll = ll.lower()
    if ll == 'debug':
        return logging.DEBUG
    if ll == 'info':
        return logging.INFO
    return logging.WARNING


def main():
    parser = argparse.ArgumentParser(description='xpctl server')
    parser.add_argument('--ll', help='Log level', type=str, default='INFO')
    parser.add_argument('--backend', help='backend', type=str, default='mongo')
    parser.add_argument('--cred', help='credential for backend',
                        default=os.path.expanduser('~/xpctlcred-mongo-local.json'))
    parser.add_argument('--user', help='user for backend')
    parser.add_argument('--passwd', help='user for backend')
    parser.add_argument('--dbhost', help='host for backend')
    parser.add_argument('--dbport', help='port for backend')
    parser.add_argument('--port', help='port', default='5310')
    args = parser.parse_args()
    
    logging.basicConfig(level=get_logging_level(args.ll))
    app = connexion.App(__name__, specification_dir='./swagger/')
    if args.user is not None:
        d = {
            'user': args.user,
            'passwd': args.passwd,
            'dbhost': args.dbhost,
            'dbport': args.dbport
        }
    else:
        d = read_config_file(args.cred)
    d.update({'dbtype': args.backend})
    app.app.backend = ExperimentRepo().create_repo(**d)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'xpctl'})
    app.run(port=args.port)


if __name__ == '__main__':
    main()
