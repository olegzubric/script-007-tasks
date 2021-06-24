#!/usr/bin/env python2
import argparse
import json
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
    parser.add_argument(
        '-f', '--folder', default=os.path.join(os.getcwd(), 'data'),
        help="working directory (default: 'data' folder)")

    return parser


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
    path = params.folder
    FileService.change_dir(path)

    functions = {
        'help': command_help,
        'chdir': command_change_dir,
        'list': command_get_files,
        'create': command_create_file,
        'get': command_get_file_data,
        'delete': command_delete_file,
        'exit': command_exit,
    }

    command_help()
    while True:
        try:
            command = raw_input('Input command: ')

            def cmd_unknown():
                print("Unknown command: {}".format(command))

            result = functions.get(command, cmd_unknown)()

            print(json.dumps({
                'status': 'success',
                'result': result,
            }, indent=2, sort_keys=True, default=StrUtils.json_serialize_helper))

        except Exception as err:
            print(json.dumps({
                'status': 'error',
                'result': str(err),
            }, indent=2, sort_keys=True, default=StrUtils.json_serialize_helper))


if __name__ == '__main__':
    main()
