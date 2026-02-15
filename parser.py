import requests
from bs4 import BeautifulSoup
import time

def get_news_from_section(section_url, filename):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    # 1. Получаем главную страницу раздела
    response = requests.get(section_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 2. Находим ссылки на новости (на Mail.ru это обычно ссылки с классом 'newsitem__title' или похожими)
    # Находим все ссылки на статьи на странице
    links = []
    # Ищем ссылки в заголовках новостей
    items = soup.find_all('a', class_='newsitem__title')[:10] # берем первые 10
    
    # Если верстка изменилась, можно искать все ссылки, ведущие на /story/ или /politics/ и т.д.
    if not items:
        items = soup.find_all('a', class_='link_flex')[:10]

    for item in items:
        href = item.get('href')
        if href.startswith('/'):
            links.append('https://news.mail.ru' + href)
        else:
            links.append(href)

    # 3. Собираем текст из каждой новости
    all_text = ""
    for link in links:
        try:
            res = requests.get(link, headers=headers)
            article_soup = BeautifulSoup(res.text, 'html.parser')
            
            # Ищем заголовок
            title = article_soup.find('h1').get_text(strip=True) if article_soup.find('h1') else "Без заголовка"
            
            # Ищем основной текстовый блок (на Mail.ru это часто класс 'article__text')
            article_block = article_soup.find('div', class_='article__text')
            if article_block:
                # Извлекаем все параграфы
                paragraphs = article_block.find_all('p')
                text = "\n".join([p.get_text(strip=True) for p in paragraphs])
                
                all_text += f"ЗАГОЛОВОК: {title}\nССЫЛКА: {link}\nТЕКСТ:\n{text}\n\n"
                all_text += "="*50 + "\n\n"
            
            time.sleep(1) # Небольшая пауза, чтобы не заблокировали
        except Exception as e:
            print(f"Ошибка при парсинге {link}: {e}")

    # 4. Сохраняем в файл
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(all_text)
    print(f"Файл {filename} успешно создан.")

# Запуск для трех разделов
sections = {
    "https://news.mail.ru": "politics_news.txt",
    "https://news.mail.ru": "economics_news.txt",
    "https://news.mail.ru": "society_news.txt"
}

for url, file in sections.items():
    print(f"Парсим раздел: {url}")
    get_news_from_section(url, file)
