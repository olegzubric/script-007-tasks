
# Общие моменты 

Делайте изменения в ветке `feature_py2py3`.

# Сделать код совместимый с обеими версиями Python 2.x и 3.x

Выполните миграцию по шагам:

1. Запустите автотесты и убедитесь, что они все проходят.

2. Установите модуль `future`.

Добавьте `future` в `requirements.txt` и выполните:

```console
$ pip install --upgrade -r requirements.txt
```

3. Улучшите код для версии 2.x:

Ознакомтесь с изменениями:

```console
$ futurize --stage1 main.py server server/tests utils
```

Примените изменения:

```console
$ futurize -w -n --stage1 main.py server server/tests utils
```

Команда `git diff` также помогает увидеть сделанные изменения.

Выполните тесты на Python 2.x и запустите программу, чтобы проверить её работоспособность.

4. Улучшите код, чтобы использовать поведение из версии 3.x:

Ознакомтесь с изменениями:

```console
$ futurize --stage2 main.py server server/tests utils
```

Примените изменения:

```console
$ futurize -w -n --stage2 main.py server server/tests utils
```

Команда `git diff` также помогает увидеть сделанные изменения.

При необходимости подправьте программу. 

Выполните тесты на Python 2.x и запустите программу, чтобы проверить её работоспособность.

Создайте виртуальное окружение для Python 3.x. Активируйте его.
Установите необходимые зависимости из `requirements.txt`. 
Выполните тесты на Python 3.x и запустите программу, чтобы проверить её работоспособность.
Обновите shebang (`#!`) до использования python:

```text
#!/usr/bin/env python
```

# Дополнительное задание

[comment]: <> (Use Pylint to help make sure you don’t regress on your Python 3 support &#40;python -m pip install pylint&#41;)

[comment]: <> (Once your dependencies are no longer blocking you, use continuous integration to make sure you stay compatible with Python 2 & 3 &#40;tox can help test against multiple versions of Python; python -m pip install tox&#41;)

[comment]: <> (Consider using optional static type checking to make sure your type usage works in both Python 2 & 3 &#40;e.g. use mypy to check your typing under both Python 2 & Python 3; python -m pip install mypy&#41;.)
