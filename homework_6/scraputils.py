import requests
from bs4 import BeautifulSoup
import re
import time
def extract_news(parser):
    """ Extract news from a given web page """

    news_list = []
    table_list = parser.table.findAll('table')[1]
    list_of_titles = table_list.findAll('a', class_='storylink') #создаем список названий
    list_of_info = table_list.findAll('td', class_='subtext') #информация по новости

    for i in range(len(list_of_titles)): #цикл который  бегает по инфе и собирает (отсеивает ненужную инфу)
        title = list_of_titles[i].text
        try:
            author = list_of_info[i].find('a', 'hnuser').text
        except AttributeError:
            author = 'author is not specified'
        try:
            points = list_of_info[i].find('span', 'score').text.split()[0]
        except AttributeError:
            points = 'author is not specified'
        comments = list_of_info[i].find(string=[re.compile('comment'), re.compile('discuss')])
        if not comments or comments == 'discuss':
            comments = 0
        else:
            comments = comments.split()[0]
        url = list_of_titles[i].get('href')
        if not url:
            print(f"url is not specified")

        news_list.append({
            'author': author,
            'points': points,
            'title': title,
            'url': url,
            'comments': comments
        }) #создаем словарь значений

    return news_list


def extract_next_page(parser): #функция которая перелистывает страницу
    """ Extract next page URL """
    next_page_news = parser.table.findAll('a', 'morelink')
    next_page = next_page_news[0]['href']
    return next_page

def get_news(url, n_pages=1): #функция дана (почитай)
    """ Collect news from a given web page """
    news = [] #у нас есть список, в который мы загружаем наши новости (список из словарей)
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
        time.sleep(3)
    return news
print(get_news('https://news.ycombinator.com/', 3))
