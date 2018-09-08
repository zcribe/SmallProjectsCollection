import scrapy
from scrapy_splash import SplashRequest


class PrismaSpider(scrapy.Spider):
    name = "prisma"

    start_urls = ['https://www.prismamarket.ee/products']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        pass
# response.body is a result of render.html call; it
# contains HTML processed by a browser.
# ...
