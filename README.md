# Python скрипт для информации о городах

## Текст задания

```plaintext
Если человек написал любое ip в консоль она - напишет страну, город, валюту, также откроет браузер с google картой и данным ip
```

## Установка и запуск

Перед запуском, убедитесь, что у вас установлен requests

```plaintext
pip install requests
```

Импорты проекта:

```py
import requests
import webbrowser
import os
import tempfile
import http.server
import socketserver
import os
import re
import csv
```

Для запуска:

- Склонируйте репозиторий
  - `git clone https://github.com/kotazzz/citydata`
- Перейдите в папку
  - `cd citydata`
- Запустите файл
  - `python main.py

## Использование

После запуска вам будет предложено написать IPv4 адрес. Напишите адрес в формате `1.2.3.4` или напишите `my`, что бы получить инфомрацию о вашем айпи. После сбора данных, браузер с отчетом должен открыться автоматически. Если этого не произошло, то перейдите на сайт вручную: `http://localhost:8000`
