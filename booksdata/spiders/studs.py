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
    name = "studs"
    allowed_domains = ["grownbrilliance.com"]
    start_urls = ["https://www.grownbrilliance.com/"]

    async def start(self):
        urls = [
            # "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            # "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
            "https://www.grownbrilliance.com/diamond-stud-earrings"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = f"studs-{page}.html"
        bookdetail = {}

        # Save content as a file
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")
        card = response.css(".nproduct")
        for card in card:
            title = card.css("nproduct_name::text").get()
            print(title)

            image = card.css(".detail_link .product_thumb")    
            image = image.attrib['src']
            print(image.attrib['src'])

            # rating = card.css("p.star-rating").attrib['class'].split()[-1]
            # # print(rating)

            # price = card.css(".price_color::text").get()
            # # print(price)

            # availability = card.css(".availability")
            # if len(availability.css(".icon-ok")) > 0:
            #     inStock = True
            # else:
            #     inStock = False

            # insertToDb(page, title, rating, image, price, inStock)