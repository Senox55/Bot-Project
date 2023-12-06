import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'}


def get_game_review(id, language, page_count_comments):
    comment_list = []

    cursor = ''
    i = 0
    while True:
        url = f'https://steamcommunity.com/app/{id}/homecontent/'
        params = {
            'userreviewsoffset': i * 10,
            'p': i + 1,
            'workshopitemspage': i + 1,
            'readytouseitemspage': i + 1,
            'mtxitemspage': i + 1,
            'itemspage': i + 1,
            'screenshotspage': i + 1,
            'videospage': i + 1,
            'artpage': i + 1,
            'allguidepage': i + 1,
            'webguidepage': i + 1,
            'integeratedguidepage': i + 1,
            'discussionspage': i + 1,
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
        if i > 0:
            params['userreviewscursor'] = cursor
        html = requests.get(url, headers=headers, params=params).text
        soup = BeautifulSoup(html, 'html.parser')
        reviews = soup.find_all('div', {'class': 'apphub_Card'})

        if not reviews or i == page_count_comments:
            break

        comment_section = [review.find('div', {'class': 'apphub_CardTextContent'}) for review in reviews]
        comment = [''.join(review.find_all(string=True, recursive=False)).strip() for review in comment_section]
        cursor = soup.find_all('form')[0].find('input', {'name': 'userreviewscursor'})['value']
        comment_list.extend(comment)
        i += 1

    return comment_list


def write_comments_in_csv(game_id, game_name, page_count_comments, language='default'):
    with open('steam_comments.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')

        for comment in get_game_review(game_id, language, page_count_comments):
            writer.writerow([game_id, game_name, comment])


write_comments_in_csv(730, 'Counter-Strike 2', 10)
write_comments_in_csv(570, 'Dota 2', 10)
write_comments_in_csv(252490, 'Rust', 10)
write_comments_in_csv(297000, 'Heroes of Might & Magic III', 10)


