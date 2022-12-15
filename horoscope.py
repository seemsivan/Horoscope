""" get_horoscopes function returns horoscope strings
between first_date and last_date for your horoscope sign"""

import datetime
import requests
from admin import ACCESS_TOKEN

ALL_SIGNS = {'овен': '♈', 'телец': '♉', 'близнецы': '♊', 'рак': '♋', 'лев': '♌', 'дева': '♍',
             'весы': '♎', 'скорпион': '♏', 'стрелец': '♐',
             'козерог': '♑', 'водолей': '♒', 'рыбы': '♓'
             }
DATE_1 = '01.01.2022'
DATE_2 = '04.01.2022'
GROUP_ID = '193489972'
MAX_NUM_POSTS_FOR_RESPONSE = 99
GROUP_NAME = 'neural_horo'


def get_post_data_and_date(url):
    """Return horoscope post texts and their dates in 2 lists by url"""
    post_texts = []
    post_dates = []
    response = requests.get(url).json()
    for j in range(len(response['response']['items'])):
        post_text = response['response']['items'][j]['text']
        post_date = datetime.datetime.fromtimestamp(
            response['response']['items'][j]['date']
        ).replace(hour=0, minute=0, second=0)
        post_date = datetime.datetime.strptime(str(post_date), '%Y-%m-%d %H:%M:%S').timestamp()
        post_texts.append(post_text)
        post_dates.append(post_date)
    return post_texts, post_dates


def get_horoscopes(first_date, last_date, horoscope_sign):
    """Return list of horoscope strings between first_date and last_date for horoscope_sign"""
    horoscope = []
    day_from = datetime.datetime.strptime(first_date, '%d.%m.%Y')
    day_from_timestamp = datetime.datetime.strptime(first_date, '%d.%m.%Y').timestamp()
    day_to_timestamp = datetime.datetime.strptime(last_date, '%d.%m.%Y').timestamp()
    today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_date_timestamp = today_date.timestamp()
    delta_days = (today_date - day_from).days  # разница между сегодня и самой ранней датой
    offset = 0
    for i in range(delta_days // MAX_NUM_POSTS_FOR_RESPONSE + 1):
        url = (
			f"https://api.vk.com/method/wall.get"
			f"?owner_id=-{GROUP_ID}"
			f"&domain={GROUP_NAME}&offset={offset}&count={MAX_NUM_POSTS_FOR_RESPONSE}"
			f"&filter=all&access_token={ACCESS_TOKEN}&v=5.131"
		)
        post_texts, post_dates = get_post_data_and_date(url)
        for date in range(len(post_dates)):
            if day_from_timestamp <= post_dates[date] <= day_to_timestamp:
                if today_date_timestamp < day_to_timestamp:
                    raise KeyError('Нет гороскопа для будущего, попробуйте другую дату.')
                if post_texts[date][0] == '♈':  # сравниваем 1ый текстовый символ с знаком гороскопа
                    text = post_texts[date].split('\n\n')
                    for elem in text:
                        if elem[0] == ALL_SIGNS[horoscope_sign]:  # строки с нужным знаком зодиака
                            horoscope.append(elem)
        offset += MAX_NUM_POSTS_FOR_RESPONSE
    return horoscope


if __name__ == "__main__":
    print('\n'.join(get_horoscopes(DATE_1, DATE_2, 'дева')))
