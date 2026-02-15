import requests
from bs4 import BeautifulSoup
import time

def get_news_from_section(section_url, filename):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(section_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Поиск ссылок на новости (селекторы могут меняться, проверьте код страницы)
    links = [a['href'] for a in soup.find_all('a', class_='newsitem__title')[:10]]
    
    with open(filename, 'w', encoding='utf-8') as f:
        for link in links:
            if not link.startswith('http'): link = 'https://news.mail.ru' + link
            
            article_res = requests.get(link, headers=headers)
            article_soup = BeautifulSoup(article_res.text, 'html.parser')
            
            # Извлекаем заголовок и текст статьи
            title = article_soup.find('h1').get_text(strip=True)
            # Текст обычно в блоке с классоm article__text или подобным
            content = article_soup.find('div', class_='article__text')
            text = content.get_text(separator=' ', strip=True) if content else "Текст не найден"
            
            f.write(f"ЗАГОЛОВОК: {title}\nТЕКСТ: {text}\n{'-'*50}\n\n")
            time.sleep(1) # Задержка, чтобы не заблокировали

# Разделы для парсинга
sections = {
    "politics.txt": "https://news.mail.ru",
    "economics.txt": "https://news.mail.ru",
    "society.txt": "https://news.mail.ru"
}

for file, url in sections.items():
    print(f"Парсим {url}...")
    get_news_from_section(url, file)
