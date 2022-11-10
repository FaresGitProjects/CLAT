import sys
import logging
import scrapy
from colorama import Fore
from scrapy.utils.log import configure_logging
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings



buy_query_list = []
grocery_list = []

class ShopSpider(scrapy.Spider):
    name = "Aspider"
    start_urls = [f"https://www.amazon.com/s?k={query}" for query in buy_query_list]

    def parse(self, response):
        # print(self.start_urls)
        # print(response)

        # b = BeautifulSoup(str(response.text.encode("utf-8")), "lxml")
        # f = open("ShopScraper/dump.html", "w")
        # f.write(b.prettify())
        # f.close()

        # print("ENTERED PARSE ********************************************************************************************************")
        curr_min = {"price": sys.maxsize, "quantity": 0, "description": "N/A", "*debug*-param":"default" }

        product_info_list = response.css("div.a-section, div.a-spacing-none, div.a-spacing-small, div.puis-padding-right-small, div.puis-padding-right-micro")
        
        for product_info in product_info_list:
            price = product_info.css("span.a-price span.a-offscreen::text").get()
            quant = product_info.css("span.a-size-small.a-color-information.puis-medium-weight-text::text").get()
            descr = product_info.css("span.a-text-normal::text").get()

            yielded = {
                "price": float(price.replace(",","").replace("$","")) if price != None else sys.maxsize,
                "quantity": quant,
                "description": descr,
                "*debug*-param": response.url
            }

            if 0 < yielded["price"] < curr_min["price"] and descr != None:
                curr_min = yielded
            
        grocery_list.append(curr_min)
        yield curr_min


if __name__ == "__main__":

    configure_logging(install_root_handler=True)
    logging.disable(50)  # CRITICAL = 50

    print(Fore.YELLOW + "\nWelcome to the Command-Line Amazon Thrifter - CLAT!\n\n \
    Enter what items your looking for and CLAT will try to\n \
    find the cheapest stuff on Amazon for you!\n" + Fore.RESET)
    num_items = int(input("How many items are in your to-do list? : ")) #7

    for i in range(1, num_items+1):
        query = input(f"Enter item #{i}: ")
        buy_query_list.append(query)

    # buy_query_list = ["shampoo", "Vitamin D gummies", "keyring", "iphone charger", "paper", "pony toy", "Book \"harry potter and the sorcerer's stone\""]
    # buy_query_list = ["keyring", "Book \"harry potter and the sorcerer's stone\"" ]

    # print(buy_query_list)
    # print([f"https://www.amazon.com/s?k={query}" for query in buy_query_list])
    print("\n.........Executing Spiders")
    print(".........Fetching Settings")
    process = CrawlerProcess(settings=get_project_settings())
    print(".........Initiate Crawling")

    process.crawl(ShopSpider, start_urls=[f"https://www.amazon.com/s?k={query}" for query in buy_query_list])
    process.start()

    print(".........Complete!\n")
    print(Fore.LIGHTGREEN_EX+"*---- Grocery List ----*\n" + Fore.RESET)
    
    for i in range(len(grocery_list)):


        desc = grocery_list[i]["description"]
        price = grocery_list[i]["price"]
        quant = grocery_list[i]["quantity"]
        debug = grocery_list[i]["*debug*-param"]
        print(Fore.LIGHTYELLOW_EX+ f"Item {i+1}:   {desc[:50] if desc != None else 'No Description Found'}..." + Fore.RESET)
        print(Fore.YELLOW+f"--- Price:    {price if price != sys.maxsize else 'No Price Found'}")
        print(f"--- Quantity: {quant if quant != None else 'No Quantity For This Item'}") if quant != None else "pass"
        print(f"--- debug-param: {debug}") if desc == None else "pass"
        print("\n" + Fore.RESET)

