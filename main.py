import requests
from bs4 import BeautifulSoup
import time

# Добавляем "заголовок", чтобы сайт не блокировал нас
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

sections = {
    "politics": "https://news.mail.ru",
    "economics": "https://news.mail.ru",
    "society": "https://news.mail.ru"
}

def parse_section(name, url):
    print(f"Ищу новости в разделе: {name}...")
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем все ссылки на новости
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            # На Mail.ru ссылки на новости обычно начинаются с /news/ или имеют полный адрес
            if '/news/' in href:
                if not href.startswith('http'):
                    href = 'https://news.mail.ru' + href
                
                if href not in links:
                    links.append(href)
            
            if len(links) == 10:
                break

        if not links:
            print(f"Ошибка: Не удалось найти ссылки в разделе {name}. Попробуй проверить URL.")
            return

        with open(f"{name}.txt", "w", encoding="utf-8") as file:
            for link in links:
                print(f"Читаю статью: {link}")
                res = requests.get(link, headers=headers)
                article_soup = BeautifulSoup(res.text, 'html.parser')
                
                # На Mail.ru текст статьи обычно лежит в блоках с классом article__item
                title = article_soup.find('h1')
                # Собираем все параграфы текста
                paragraphs = article_soup.find_all(['p', 'div'], class_='article__item')
                
                if title:
                    file.write("ЗАГОЛОВОК: " + title.get_text(strip=True) + "\n\n")
                
                content_found = False
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text:
                        file.write(text + "\n")
                        content_found = True
                
                if not content_found:
                    # Запасной вариант, если класс изменился
                    all_p = article_soup.find_all('p')
                    for p in all_p:
                        file.write(p.get_text(strip=True) + "\n")

                file.write("\n" + "="*30 + "\n\n")
                time.sleep(1) # Небольшая пауза, чтобы сайт нас не забанил

    except Exception as e:
        print(f"Произошла ошибка при работе с разделом {name}: {e}")

for name, url in sections.items():
    parse_section(name, url)

print("Процесс завершен. Проверь файлы!")
