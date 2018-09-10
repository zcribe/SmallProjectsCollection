import scrapy
from scrapy_splash import SplashRequest


class PrismaSpider(scrapy.Spider):
    name = "coop"
    start_urls = ['https://ecoop.ee/et/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        food_drink = "https://www.prismamarket.ee/products"
        yield SplashRequest(food_drink, self.parse_category, args={'wait': 0.5})
