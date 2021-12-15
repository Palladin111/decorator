import datetime
import requests
from bs4 import BeautifulSoup
import re


def logger_decor(path_log_file):
    def _logger_decor(old_function):
        def new_function(*args, **kwargs):
            start_date = datetime.datetime.now().strftime('%d - %m - %Y')
            start_time = datetime.datetime.now().strftime('%H - %M - %S')
            result = old_function(*args, **kwargs)
            file_name = old_function.__name__ + '.txt'
            path_file_name = path_log_file + file_name
            if kwargs:
                with open(path_file_name, 'w', encoding='utf-8') as document:
                    if kwargs:
                        document.write(f'Date call function: {start_date} and time call function: {start_time}'
                                       f' \nName functions: {old_function.__name__} '
                                       f' \nArguments functions: {args}, {kwargs}\nReturn values functions: {result}')
            else:
                with open(path_file_name, 'w', encoding='utf-8') as document:
                    document.write(f'Date call function: {start_date} and time call function: {start_time}'
                                   f' \nName functions: {old_function.__name__} '
                                   f' \nArguments functions: {args}\nReturn values functions: {result}')
            return result
        return new_function
    return _logger_decor



@logger_decor('C:/logs/')
def webscrapping(a, b, c, d):
    MY_HUBS = [a, b, c, d]

    response = requests.get("https://habr.com/ru/all/", timeout=15, headers={"User-Agent":"Mozilla/5.0 "})
    response.raise_for_status()
    text = response.text

    soup = BeautifulSoup(text, features="html.parser")
    articles = soup.find_all('article')

    title_1 = []
    list = []
    for article in articles:
        for hub in MY_HUBS:
            pattern_hub = re.compile("({})".format(hub))
            result = pattern_hub.findall(article.text)
            if hub in result:
                date = article.find('time').attrs.get('title')
                title = article.find('h2')
                link = title.find('a').attrs.get('href')
                url = "https://habr.com" + link
                if title.text not in title_1:
                    title_1.append(title.text)
                    list.append(f'{date[0:10]} - {title.text} - {url}')
                    print(f'{date[0:10]} - {title.text} - {url}')
    return list

webscrapping('человек', 'игры', 'web', 'python')

