import requests
from bs4 import BeautifulSoup

# Список разделов (можно менять ссылки на нужные тебе)
sections = {
    "politics": "https://news.mail.ru",
    "economics": "https://news.mail.ru",
    "society": "https://news.mail.ru"
}

def parse_section(name, url):
    print(f"Парсим раздел: {name}...")
    # 1. Получаем главную страницу раздела
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 2. Ищем ссылки на статьи (находим все ссылки с классом новостей)
    links = []
    for a in soup.find_all('a', href=True):
        if '/news/' in a['href'] and a['href'].startswith('https://news.mail.ru'):
            if a['href'] not in links:
                links.append(a['href'])
        if len(links) == 10: break # Нам нужно только 10

    # 3. Заходим в каждую статью и вынимаем текст
    with open(f"{name}.txt", "w", encoding="utf-8") as file:
        for link in links:
            res = requests.get(link)
            article_soup = BeautifulSoup(res.text, 'html.parser')
            
            # Ищем заголовок и основной текст
            title = article_soup.find('h1')
            paragraphs = article_soup.find_all('p')
            
            if title:
                file.write(title.get_text() + "\n")
            for p in paragraphs:
                file.write(p.get_text() + " ")
            file.write("\n\n" + "="*30 + "\n\n")

# Запуск парсера для всех разделов
for name, url in sections.items():
    parse_section(name, url)

print("Готово! Проверь папку с файлами.")
