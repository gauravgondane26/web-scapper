import scrapy
from pathlib import Path
from pymongo import MongoClient
import datetime

username = "gauravgondane1"
password = "oi5B2tXIG4kKRqUM"

client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.khnkpqj.mongodb.net/")
db = client.scrapy

def insertToDb(page, title, rating, image, price, inStock):
    collecion = db[page]
    doc = {
        "title": title,
        "rating": rating,
        "image": image,
        "price": price,
        "inStock": inStock,
        "date": datetime.datetime.now(tz=datetime.timezone.utc)
    }

    inserted = collecion.insert_one(doc)
    return inserted.inserted_id

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    async def start(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"books-{page}.html"
        bookdetail = {}

        # Save content as a file
        # Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
        card = response.css(".product_pod")
        for card in card:
            title = card.css("h3>a::text").get()
            # print(title)

            image = card.css(".image_container img")    
            image = image.attrib['src'].replace("../../../../media", "https://books.toscrape.com/media")
            # print(image.attrib['src'])

            rating = card.css("p.star-rating").attrib['class'].split()[-1]
            # print(rating)

            price = card.css(".price_color::text").get()
            # print(price)

            availability = card.css(".availability")
            if len(availability.css(".icon-ok")) > 0:
                inStock = True
            else:
                inStock = False

            insertToDb(page, title, rating, image, price, inStock)