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


# write_comments_in_csv(730, 'Counter-Strike 2', 1, 300)
# write_comments_in_csv(570, 'Dota 2', 1, 300)
# write_comments_in_csv(252490, 'Rust', 1, 300)
# write_comments_in_csv(297000, 'Heroes of Might & Magic III', 1, 300)
# write_comments_in_csv(710154, 'Lethal Company', 1, 300)
# write_comments_in_csv(739630, 'Phasmophobia', 1, 300)
# write_comments_in_csv(218620, 'PAYDAY 2', 1, 300)
# write_comments_in_csv(105600, 'Terraria', 1, 300)
# write_comments_in_csv(21357, 'Path of Exile', 1, 300)
# write_comments_in_csv(221100, 'DayZ', 1, 300)
# write_comments_in_csv(2073850, 'THE FINALS', 1, 300)
# write_comments_in_csv(431960, 'Wallpaper Engine', 1, 300)
# write_comments_in_csv(493520, 'GTFO', 1, 300)
# write_comments_in_csv(620, 'Portal 2', 1, 300)
# write_comments_in_csv(1118200, 'People Playground', 1, 300)
# write_comments_in_csv(1794680, 'Vampire Survivors', 1, 300)
# write_comments_in_csv(413150, 'Stardew Valley', 1, 300)
# write_comments_in_csv(1145360, 'Hades', 1, 300)
# write_comments_in_csv(400, 'Portal', 1, 300)
# write_comments_in_csv(2420510, 'HoloCure', 1, 300)
# write_comments_in_csv(546560, 'Half-Life: Alyx', 1, 300)
# write_comments_in_csv(2231450, 'Pizza Tower', 1, 300)
# write_comments_in_csv(1089980, 'The Henry Stickmin Collection', 1, 300)
# write_comments_in_csv(227300, 'Euro Truck Simulator 2', 1, 300)
# write_comments_in_csv(646570, 'Slay the Spire', 1, 300)
# write_comments_in_csv(1229490, 'ULTRAKILL', 1, 300)
# write_comments_in_csv(1144400, 'Senren＊Banka', 1, 300)
# write_comments_in_csv(433340, 'Slime Rancher', 1, 300)
# write_comments_in_csv(2050650, 'Resident Evil 4', 1, 300)
# write_comments_in_csv(460950, 'Katana ZERO', 1, 300)
# write_comments_in_csv(220, 'Half-Life 2', 1, 300)
# write_comments_in_csv(4000, 'Garrys Mod', 1, 300)
# write_comments_in_csv(205100, 'Dishonored', 1, 300)
# write_comments_in_csv(1288310, 'Firework', 1, 300)
# write_comments_in_csv(1332010, 'Stray', 1, 300)
# write_comments_in_csv(883710, 'Resident Evil 2', 1, 300)
# write_comments_in_csv(219150, 'Hotline Miami', 1, 300)
# write_comments_in_csv(1942280, 'Brotato', 1, 300)



