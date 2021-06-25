#!/usr/bin/env python3
import argparse
import logging
import logging.config
import os

from aiohttp import web

from server.WebHandler import WebHandler


def commandline_parser():
    """Command line parser.

    Parse port and working directory parameters from command line.

    Returns:
        argparse.ArgumentParser
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', default=os.path.join(os.getcwd(), 'data'), type=str,
                        help="working directory (default: 'data' folder)")
    parser.add_argument('--log-level', default='warning', choices=['debug', 'info', 'warning', 'error'],
                        help='Log level to console (default is warning)')
    parser.add_argument('-l', '--log-file', type=str, help='Log file.')
    # TODO: add --port parameter

    return parser


def setup_logger(level='NOTSET', filename=None):
    config = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': level,
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
    if filename:
        config['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'encoding': 'UTF-8',
            'formatter': 'default',
            'filename': filename,
        }
        config['root']['handlers'].append('file')
    logging.config.dictConfig(config)


def main():
    """Entry point of app.

    Get and parse command line parameters and configure web app.

    Command line options:
    -f --folder - working directory (absolute or relative path, default: current app folder).
    -p --port - port (default: 8080).
    -h --help - help.
    """

    parser = commandline_parser()
    params = parser.parse_args()
    setup_logger(level=logging.getLevelName(params.log_level.upper()), filename=params.log_file)

    handler = WebHandler(params.folder)
    app = web.Application()
    app.add_routes([
        web.get('/', handler.handle),
        # TODO: add more routes
    ])
    logging.basicConfig(level=logging.INFO)
    web.run_app(app, port=params.port)


if __name__ == '__main__':
    main()
