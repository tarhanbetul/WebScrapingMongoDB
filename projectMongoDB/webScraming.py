import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
from pymongo import MongoClient
import pickle
import time
from datetime import datetime

TEMP_DATA_FILE = "temp_data.pkl" # bulunduğu dizinin (dosyanın) yolunu veriniz!
client = MongoClient('mongodb://localhost:27017/')
db = client['smartmaple']
#database_name = "smartmaple"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}



def save_data(book_list):
    print("Dosya kaydediliyor...")

    with open(TEMP_DATA_FILE, "wb") as f:
        pickle.dump(book_list, f)

    print("Dosya kaydedildi.")

def load_data():
    try:
        with open(TEMP_DATA_FILE, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

def scrape(site, collection):
    try:
        page = requests.get(site, headers=headers)
        pageContent = BeautifulSoup(page.content, 'html.parser')

        if site == "https://www.kitapyurdu.com/kategori/kitap-kisisel-gelisim/341.html":

            book_title = pageContent.find_all("div", attrs={"class": "name ellipsis"})
            book_price = pageContent.find_all("span", attrs={"class":"value"})
            book_publisher = pageContent.find_all("div", attrs={"class": "publisher"})
            book_writers = pageContent.find_all("div", attrs={"class": "author compact ellipsis"})

        else:

            book_title = pageContent.find_all("a", attrs={"class":"fl col-12 text-description detailLink"})
            book_price = pageContent.find_all("div", attrs={"class":"col col-12 currentPrice"})
            book_publisher = pageContent.find_all("a", attrs={"class":"col col-12 text-title mt"})
            book_writers = pageContent.find_all("a", attrs={"id":"productModelText"})

        insert(collection, book_title, book_price, book_publisher, book_writers)

    except requests.exceptions.MissingSchema:
        print(f"Geçersiz URL: '{site}' URL'si düzgün biçimde girilmemiş.")
    except requests.exceptions.RequestException as e:
        print(f"URL'ye ulaşırken bir hata oluştu: {e}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

def insert(collection, book_title, book_price, book_publisher, book_writers):
    book_list = []

    for title, price, publisher, writers in zip(book_title, book_price, book_publisher, book_writers):
        book_data = {
            "title": title.text.strip(),
            "price": price.text.replace('\n','') if site == "https://www.kitapsepeti.com/cizgi-roman" else price.text.strip(),
            "publisher": publisher.text.strip(),
            "writers": writers.text.strip()
        }
        # Verileri koleksiyona ekleyin.
        collection.insert_one(book_data)
        book_list.append(book_data)

    if len(book_list) > 0:
        save_data(book_list)

if __name__ == "__main__":

    urls = [
        "https://www.kitapyurdu.com/kategori/kitap-kisisel-gelisim/341.html",
        "https://www.kitapsepeti.com/cizgi-roman"
    ]
    while True:
        # Şu anki saat ve dakika bilgisini alalım
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute

        # Hedef saat ve dakikayı belirleyelim (örneğin 12:00)
        target_hour = 12
        target_minute = 0

        # Hedef saat ve dakikaya gelene kadar bekle
        if current_hour < target_hour or (current_hour == target_hour and current_minute < target_minute):
            sleep_time_seconds = (target_hour - current_hour) * 3600 + (target_minute - current_minute) * 60
            time.sleep(sleep_time_seconds)
        for site in urls:
            if site == "https://www.kitapyurdu.com/kategori/kitap-kisisel-gelisim/341.html":
                collection = db["kitapyurdu"]
            else:
                collection = db["kitapsepeti"]
            scrape(site, collection)



