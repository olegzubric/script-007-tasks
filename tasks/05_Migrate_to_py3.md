
# Общие моменты 

Делайте изменения в ветке `feature_py3`.

# Портировать код на Python 3.x

Выполните миграцию по шагам:

1. Запустите автотесты и убедитесь, что они все проходят.

2. Установите Python 3.

3. Создайте виртуальное окружение:

```console
$ python -m venv venv3
$ venv\Scripts\Activate.bat  # Windows CMD
$ venv/Scripts/Activate.ps1  # Windows PowerShell
$ source venv/bin/activate   # Linux
$ pip install --upgrade pip
```

4. Установите `2to3`:

```console
$ pip install --upgrade 2to3
```

5. Обновление кода

Ознакомтесь с предлагаемыми изменениями:

```console
$ 2to3 main.py server server/tests utils
```

Примените изменения:

```console
$ 2to3 -w -n main.py server server/tests utils
```

Команда `git diff` также помогает увидеть сделанные изменения.

Выполните тесты на Python 3.x и запустите программу, чтобы проверить её работоспособность. При необходимости 
доработайте код. 
Обновите shebang (`#!`) до использования python3:

```text
#!/usr/bin/env python3
```

Добавьте Type Hints к соответствующим фукнциям.

# Документация

[2to3 - Automated Python 2 to 3 code translation](https://docs.python.org/3/library/2to3.html)
