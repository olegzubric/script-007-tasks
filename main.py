#!/usr/bin/env python2
import argparse
import json
import logging
import logging.config
import os
import sys

import server.FileService as FileService
import utils.StrUtils as StrUtils


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


def command_change_dir():
    """Change current directory of app.

    Raises:
        RuntimeError: if directory does not exist and autocreate is False.
    """

    new_path = raw_input('Input new working directory path: ')
    return FileService.change_dir(new_path)


def command_get_files():
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
        - name (str): filename
        - create_date (datetime): date of file creation.
        - edit_date (datetime): date of last file modification.
        - size (int): size of file in bytes.
    """

    return FileService.get_files()


def command_get_file_data():
    """Get full info about file.

    Returns:
        Dict, which contains full info about file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - edit_date (datetime): date of last file modification
        - size (int): size of file in bytes

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    filename = raw_input('Input filename: ')
    return FileService.get_file_data(filename)


def command_create_file():
    """Create a new file.

    Returns:
        Dict, which contains name of created file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - size (int): size of file in bytes

    Raises:
        ValueError: if filename is invalid.
    """

    filename = raw_input('Input filename: ')
    content = raw_input('Input content: ')
    return FileService.create_file(filename, content)


def command_delete_file():
    """Delete file.

    Raises:
        RuntimeError: if file does not exist.
    """

    filename = raw_input('Input filename: ')
    return FileService.delete_file(filename)


def command_help():
    print("""Commands:
help  : show this help
chdir : change working directory
list  : get list of files
create: create a file with content
get   : get a file data
delete: delete a file
exit  : exit from app
""")


def command_exit():
    sys.exit(0)


def main():
    """Entry point of app.

    Get and parse command line parameters and configure web app.

    Command line options:
    -f --folder - working directory (absolute or relative path, default: current app folder).
    -h --help - help.
    """
    parser = commandline_parser()
    params = parser.parse_args()
    setup_logger(level=logging.getLevelName(params.log_level.upper()), filename=params.log_file)

    path = params.folder
    FileService.change_dir(path)

    logging.debug('initialized')

    functions = {
        'help': command_help,
        'chdir': command_change_dir,
        'list': command_get_files,
        'create': command_create_file,
        'get': command_get_file_data,
        'delete': command_delete_file,
        'exit': command_exit,
    }

    def to_json(obj):
        return json.dumps(obj, indent=2, sort_keys=True, default=StrUtils.json_serialize_helper)

    command_help()
    while True:
        command = raw_input('Input command: ')
        try:
            def cmd_unknown():
                print("Unknown command: {}".format(command))

            result = functions.get(command, cmd_unknown)()
            logging.debug('executing %s, result %s', command, to_json(result))

            print(to_json({
                'status': 'success',
                'result': result,
            }))

        except Exception as err:
            logging.info('executing %s, face an exception %s', command, str(err))
            print(to_json({
                'status': 'error',
                'result': str(err),
            }))


if __name__ == '__main__':
    main()
