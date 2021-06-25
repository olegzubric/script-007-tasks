
# Общие моменты 

Делайте изменения в ветке `feature_web`.

# Реализуйте web-сервер

1. В файле `web.py` в функции `commandline_parser` добавьте параметр `-p/--port` со значением по умолчанию 8080. 

2.  В файле `web.py` в функции `main` добавьте маршрутизацию:

| POST   | URL               | Handler               |
| ------ | ----------------- | --------------------- |
| POST   | /change_dir       | handler.change_dir    |
| GET    | /files            | handler.get_files     |
| GET    | /files/{filename} | handler.get_file_data |
| POST   | /files            | handler.create_file   |
| DELETE | /files/{filename} | handler.delete_file   |

3. В файле `server/WebHandler.py` реализуйте корутины для обработки web-запросов.

4. Для проверки используйте скрипты из папки `test_web`.
