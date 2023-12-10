import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'}


def get_game_review(id, language, start_page_number, finish_page_number):
    comment_list = []

    cursor = ''
    while True:
        url = f'https://steamcommunity.com/app/{id}/homecontent/'
        params = {
            'userreviewsoffset': start_page_number * 10,
            'p': start_page_number + 1,
            'workshopitemspage': start_page_number + 1,
            'readytouseitemspage': start_page_number + 1,
            'mtxitemspage': start_page_number + 1,
            'itemspage': start_page_number + 1,
            'screenshotspage': start_page_number + 1,
            'videospage': start_page_number + 1,
            'artpage': start_page_number + 1,
            'allguidepage': start_page_number + 1,
            'webguidepage': start_page_number + 1,
            'integeratedguidepage': start_page_number + 1,
            'discussionspage': start_page_number + 1,
            'numperpage': 10,
            'browsefilter': 'toprated',
            'browsefilter': 'toprated',
            'appid': id,
            'appHubSubSection': 10,
            'l': 'english',
            'filterLanguage': language,
            'searchText': '',
            'forceanon': 1,
            'maxInappropriateScore': 50,
        }
        if start_page_number > 0:
            params['userreviewscursor'] = cursor
        html = requests.get(url, headers=headers, params=params).text
        soup = BeautifulSoup(html, 'html.parser')
        reviews = soup.find_all('div', {'class': 'apphub_Card'})

        if not reviews or start_page_number == finish_page_number:
            break

        comment_section = [review.find('div', {'class': 'apphub_CardTextContent'}) for review in reviews]
        comment = [''.join(review.find_all(string=True, recursive=False)).strip() for review in comment_section]
        cursor = soup.find_all('form')[0].find('input', {'name': 'userreviewscursor'})['value']
        comment_list.extend(comment)
        start_page_number += 1

    return comment_list


def write_comments_in_csv(game_id, game_name, start_page_number, finish_page_number, language='default'):
    with open('steam_comments.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')

        for comment in get_game_review(game_id, language, start_page_number, finish_page_number):
            writer.writerow([game_id, game_name, comment])


write_comments_in_csv(730, 'Counter-Strike 2', 1, 100)
write_comments_in_csv(570, 'Dota 2', 1, 100)
write_comments_in_csv(252490, 'Rust', 1, 100)
write_comments_in_csv(297000, 'Heroes of Might & Magic III', 1, 100)
