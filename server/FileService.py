import os
import time


def change_dir(path, autocreate=True):
    """Change current directory of app.

    Args:
        path (str): Path to working directory with files.
        autocreate (bool): Create folder if it doesn't exist.

    Raises:
        RuntimeError: if directory does not exist and autocreate is False.
    """

    if not os.path.exists(path):
        os.makedirs(path)
    
    os.chdir(path)


def get_files(path='./'):
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
        - name (str): filename
        - create_date (datetime): date of file creation.
        - edit_date (datetime): date of last file modification.
        - size (int): size of file in bytes.
    """
    list_of_file_dicts = []
    file_names = os.listdir(path)
    for file_name in file_names:
        file_path = os.path.join(path, file_name)
        file_dict = {
            'name': file_name,
            'create_date':  time.ctime(os.path.getctime(file_path)),
            'edit_date':  time.ctime(os.path.getctime(file_path)),
            'size': int(os.stat(file_path).st_size)
        }
        list_of_file_dicts.append(file_dict)
    return list_of_file_dicts
    

def get_file_data(filename):
    """Get full info about file.

    Args:
        filename (str): Filename.

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


def create_file(filename, content=None):
    """Create a new file.

    Args:
        filename (str): Filename.
        content (str): String with file content.

    Returns:
        Dict, which contains name of created file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - size (int): size of file in bytes

    Raises:
        ValueError: if filename is invalid.
    """

    with open(filename, 'wb') as file_handler:
        if content:
            data = bytes(content)
            file_handler.write(data)



def delete_file(filename):
    """Delete file.

    Args:
        filename (str): filename

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    pass
