import requests
import webbrowser
import os
import tempfile
import http.server
import socketserver
import os
import re
import csv

PORT = 8000

def main():
    # Для поиска данных о валюте по коду страны
    currency_data = csv.DictReader(open("codes.csv"))
    def find_currency_data(code):
        for line in currency_data:
            # Country,CountryCode,Currency,Code
            if line["CountryCode"] == code:
                return f'<b>Валюта</b>: {line["Currency"]} ({line["Code"]})'
        return f"<b>Валюта</b>: Нет данных"

    # Получение IP от пользователя
    print(
        'Введите необходимый айпи или введите "my", что бы получить информацию о своем айпи'
    )
    while True:
        user_ip = input("ip> ")
        if user_ip == "my":
            user_ip = ""
            break
        if re.findall(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", user_ip):
            break
        print("Введите конкретный IPv4 адрес в формате 255.255.255!")
    
    # Получение данных об айпи, используется API
    # Запрашиваем только: ip,country,city,region,flag,latitude,longitude,country_code
    fetch_url = f"http://ipwho.is/{user_ip}?lang=ru&fields=ip,country,city,region,flag,latitude,longitude,country_code"
    response = requests.get(fetch_url)
    if response.status_code != 200:
        print(f"Неизвестная ошибка: {response.status_code} - {response.content}")
        exit(-1)
    data: dict = response.json()
    
    # Сборка временного файла
    with tempfile.TemporaryDirectory() as tmp:    
        base = f"<h1>IP: {data['ip']}</h1>"
        # Простые поля
        prints = {
            "Страна": "country",
            "Город": "city",
            "Регион": "region",
        }
        # Сложные поля
        other = [
            f'<b>Google Maps</b>: <a href="https://www.google.com/maps/search/{data["latitude"]},{data["longitude"]}">Тут</a>',
            find_currency_data(data["country_code"]),
            f'<p><img src="{data["flag"]["img"]}" height="100px"><p>',
        ]
        
        # Базовые данные API
        base += f"<h2>Базовые данные API</h2><ul>"
        for name, key in prints.items():
            value = data[key] if key in data else "Нет данных"
            base += f"<li><b>{name}</b>: {value}</li>"
        for line in other:
            base += f"<li>{line}</li>"
        base += "</ul>"
        
        # Сырой вывод всех данных
        base += "<h2>Данные полученные от API</h2>"
        base += f"<code>{data}</code>"
        
        # Запись всего в файл
        index = os.path.join(tmp, "index.html")
        with open(index, "w", encoding="utf-8") as file:
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            <body>
                {base}
            </body>
            </html>
            """
            file.write(html)

        # Перемещаемся в временную папку и начинаем хостить там index.html на порту PORT
        os.chdir(tmp)
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", PORT), Handler)
        print(
            f"Сервер находится на порту: {PORT}\n"
            "Браузер откроется автоматический.\n"
            f"Если этого не произошло: http://localhost:{PORT}\n"
        )
        
        # Автоматически открываем браузер
        try:
            webbrowser.open(f"http://localhost:{PORT}")
            print('Браузер должен был открыться!')
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nПока!")
            httpd.shutdown()


if __name__ == "__main__":
    main()
