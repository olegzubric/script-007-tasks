#!/usr/bin/env python2
import argparse
import os
import server.FileService

def commandline_parser():
    """Command line parser.

    Parse port and working directory parameters from command line.

    Returns:
        argparse.ArgumentParser
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', help='Directory with files', default=os.getcwd())
    return parser


def command_change_dir():
    """Change current directory of app.

    Raises:
        RuntimeError: if directory does not exist and autocreate is False.
    """

    #server.FileService.change_dir()


def command_get_files():
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
        - name (str): filename
        - create_date (datetime): date of file creation.
        - edit_date (datetime): date of last file modification.
        - size (int): size of file in bytes.
    """

    file_infos = server.FileService.get_files()
    for file_info in file_infos:
        print(file_info)


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

    pass


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

    filename = raw_input('Input file name:')
    filecontent = raw_input('Input content file:')
    server.FileService.create_file(filename,filecontent)


def command_delete_file():
    """Delete file.

    Raises:
        RuntimeError: if file does not exist.
    """

    pass


def main():
    """Entry point of app.

    Get and parse command line parameters and configure web app.

    Command line options:
    -d --directory - working directory (absolute or relative path, default: current app folder).
    -h --help - help.
    """

    parser = commandline_parser()
    params = parser.parse_args()
    workDir = params.dir
    server.FileService.change_dir(workDir)
    #print ("WorkDir = " + workDir)
    while True:
        command = raw_input('Input command:')
        if command == 'create':
            command_create_file()
        elif command == 'list':
            command_get_files()
        elif command == 'get':
            command_get_file_data()
        elif command == 'delete':
            command_delete_file()
        elif command == 'exit':
            return
        else:
            print ('Unknown command')

if __name__ == '__main__':
    main()
