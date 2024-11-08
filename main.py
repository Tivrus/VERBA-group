import requests
from bs4 import BeautifulSoup
import json
import time, os

# URL для начала сбора данных
base_url = "https://quotes.toscrape.com"
page_url = "/page/"

# Список для хранения данных всех цитат
all_quotes = []


# НЕБОЛЬШОЕ ДОПОЛНЕНИЕ ДЛЯ УВИЛЕЧЕНИЯ ФУНКЦИОНАЛА
def get_author_info(author_url):
    # Функция для получения информации об авторе
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        author_title = soup.find("h3", class_="author-title").get_text(strip=True)
        author_born_date = soup.find("span", class_="author-born-date").get_text(strip=True)
        author_born_location = soup.find("span", class_="author-born-location").get_text(strip=True)
        author_description = soup.find("div", class_="author-description").get_text(strip=True)
        
        return {
            "Author_title": author_title,
            "Author_born_date": author_born_date,
            "Author_born_location": author_born_location,
            "Author_description": author_description
        }
    except AttributeError:
        return None
def InputError():
    #Функция неверного ввода
    global author_info_taker
    print("\nПолучить подробную информацию об авторах?\n1 - Да\n2 - Нет")
    author_info_taker = input("Ввод -> ")
    if author_info_taker != "1" and author_info_taker != "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Введите ликвидное значение!')
        InputError()



InputError()
page_number = 1

while True:
    # Загружаем страницу
    response = requests.get(base_url + page_url + str(page_number) + "/")
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.find_all("div", class_="quote")
    if not quotes:
        break

    # Обрабатываем каждую цитату на странице
    for index, quote in enumerate(quotes, start=1):
        # Извлекаем цитату
        quote_text = quote.find("span", class_="text").get_text(strip=True)
        author = quote.find("small", class_="author").get_text(strip=True)
        author_link = base_url + quote.find("a")["href"]

        # Извлекаем теги
        tags = []
        for tag in quote.find_all("a", class_="tag"):
            tags.append(tag.get_text(strip=True))


        if author_info_taker == "1":
            author_info = get_author_info(author_link)

            # Добавляем данные в список для записи в JSON
            all_quotes.append({
                "Quote": quote_text,
                "Author": author,
                "Author_link": author_link,
                "Tags": tags,
                "Page": page_number,
                "Position_on_page": index,
                "Author_info": author_info
            })
        else:
            all_quotes.append({
                "Quote": quote_text,
                "Author": author,
                "Author_link": author_link,
                "Tags": tags,
                "Page": page_number,
                "Position_on_page": index
            })
        time.sleep(0.1)
    page_number += 1


with open("quotes.json", "w", encoding="utf-8") as file:
    json.dump(all_quotes, file, ensure_ascii=False, indent=4)

print("Данные успешно сохранены в quotes.json")