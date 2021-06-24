# coding=utf-8
import os
import shutil

import pytest

from server import FileService




'''
@pytest.fixture(autouse=True, scope='module')
def create_existed_dir():
    existed_dir_name = 'ExistingDirectory'
    run_file_path = os.path.dirname(os.path.abspath(__file__))
    existed_dir_path = os.path.join(run_file_path, existed_dir_name)
    if not os.path.exists(existed_dir_path):
        os.mkdir(existed_dir_path)
    yield
    shutil.rmtree(existed_dir_path)
'''

@pytest.fixture(scope='module', autouse=True)
def change_test_dir(request):
    old_cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    yield
    os.chdir(old_cwd)


def helper_rm(path):
    if not os.path.exists(path):
        return

    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


@pytest.fixture(scope='session', autouse=True)
def safe_cleanup(request):
    def cleanup():
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        helper_rm('NotExistingDirectory')
        helper_rm('ExistingDirectory')

    cleanup()  # before all tests
    yield
    cleanup()  # after all tests

class Test_change_dir:
    def test_incorrect_type1(self):
        """Передать None в качестве значения

        Ожидаемый результат: возбуждение исключения TypeError
        """
        with pytest.raises(TypeError):
            FileService.change_dir(None)


    def test_incorrect_type2(self):
        """Передать значение типа int

        Ожидаемый результат: возбуждение исключения TypeError
        """
        with pytest.raises(TypeError):
            FileService.change_dir(123)

    def test_dot_dir(self):
        """Передать . в качестве значения,

        Ожидаемый результат: текущая папка не должна измениться
        """
        current_dir = os.getcwd()
        FileService.change_dir('.')
        dir_after = os.getcwd()

        assert current_dir == dir_after

    def test_incorrect_value2(self):
        """Передать .. в качестве значения

        Ожидаемый результат: возбуждение исключения ValueError
        """
        with pytest.raises(ValueError):
            FileService.change_dir('..')

    def test_incorrect_value3(self):
        """Передать ../something в качестве значения

        Ожидаемый результат: возбуждение исключения ValueError
        """
        with pytest.raises(ValueError):
            FileService.change_dir('../something')
        
    def test_existing_dir_no_create(self):
        """Перейти в каталог, который уже существует и autocreate=False

        Ожидаемый результат: текущая папка имеет имя ExistingDirectory
        """
        #run_file_path = os.path.dirname(os.path.abspath(__file__))
        #path = os.path.join(run_file_path, 'ExistingDirectory')
        #FileService.change_dir(path, autocreate=False)
        os.mkdir('ExistingDirectory')
        FileService.change_dir('ExistingDirectory', autocreate=False)
        current_dir = os.getcwd()
        assert os.path.basename(current_dir) == 'ExistingDirectory'

    def test_existing_dir_create(self):
        """Перейти в каталог, который уже существует и autocreate=True

        Ожидаемый результат: текущая папка имеет имя ExistingDirectory
        """
        os.mkdir('ExistingDirectory')
        FileService.change_dir('ExistingDirectory', autocreate=True)
        cwd = os.getcwd()
        assert os.path.basename(cwd) == 'ExistingDirectory'

    def test_non_existing_dir_no_create(self):
        """Перейти в каталог, который не существует и autocreate=False

        Ожидаемый результат: текущая папка имеет имя отличное от NotExistingDirectory
        """
        with pytest.raises(RuntimeError):
            FileService.change_dir('NotExistingDirectory', autocreate=False)
        cwd = os.getcwd()
        assert os.path.basename(cwd) != 'NotExistingDirectory'

    def test_non_existing_dir_create(self):
        """Перейти в каталог, который не существует и autocreate=True

        Ожидаемый результат: текущая папка имеет имя отличное от NotExistingDirectory
        """
        FileService.change_dir('NotExistingDirectory', autocreate=True)
        cwd = os.getcwd()
        assert os.path.basename(cwd) == 'NotExistingDirectory'
