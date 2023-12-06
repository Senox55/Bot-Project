import requests
from bs4 import BeautifulSoup
import csv
import json, urllib.request


# Функция для получения HTML-кода страницы с комментариями к игре на Steam
def get_html(url):
    response = requests.get(url)
    return response.text


# Функция для парсинга комментариев к игре на Steam
def parse_comments(data):
    comments = []
    for page in data['reviews']:
        comment = page['review']
        comments.append(comment)
    return comments


# Главная функция для получения комментариев и записи их в CSV-файл
def get_comments(game_id, game_name):
    all_comments = []
    cursor = 'AoIIPxIgNne07LsE'
    for page in range(1, 40):
        with urllib.request.urlopen(f'https://store.steampowered.com/appreviews/{game_id}?json=1&cursor={cursor}') as url:
            data = json.load(url)
            if data['success'] == 8 or cursor == data['cursor']:
                cursor = page
                continue
            print(data)
            all_comments += parse_comments(data)
            cursor = data['cursor']
            print(cursor)

    # Запись результатов в CSV-файл
    with open('steam_comments.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')

        for comment in all_comments:
            writer.writerow([game_id, game_name, comment])


if __name__ == "__main__":
    get_comments(252490, 'Rust')

