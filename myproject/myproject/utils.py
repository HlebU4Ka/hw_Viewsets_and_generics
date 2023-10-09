import re


# Функция для проверки ссылки на youtube.com
def is_youtube_link(link):
    return re.match(r'^https:\/\/www\.youtube\.com\/', link) is not None
