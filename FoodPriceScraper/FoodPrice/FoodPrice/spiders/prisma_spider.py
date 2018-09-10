import logging

import scrapy
from scrapy_splash import SplashRequest


class PrismaSpider(scrapy.Spider):
    name = "prisma"

    start_urls = ['https://www.prismamarket.ee/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.7})

    def parse(self, response):
        food_drink = "https://www.prismamarket.ee/products"
        yield response.follow(food_drink, self.parse_category)

    def parse_category(self, response):
        for href in response.xpath("//a[@class='js-category-item']/@href"):
            yield response.follow(href, self.parse_subcategory)

    def parse_subcategory(self, response):
        for href in response.xpath("//a[@class='js-category-item']/@href"):
            yield response.follow(href, self.parse_item)

    def parse_item(self, response):

        name_list = response.xpath("//div[@class='info relative clear']/div[@class='name']/text()").extract()
        logging.info(name_list)
        whole_list = response.xpath("//div[@class='js-info-price']/span[@class='whole-number ']/text()").extract()
        decimal_list = response.xpath("//div[@class='js-info-price']/span[@class='decimal']/text()").extract()
        unit_list = response.xpath("//div[@class='js-info-price']/span[@class='unit']/text()").extract()
        category = response.xpath("//h2[@class='js-products-page-name viewport category-header']/text()").extract()[0]

        price = []
        logging.info('Whole')
        logging.info(whole_list)
        for x, y, z in zip(whole_list, decimal_list, unit_list):
            price.append("{}.{}{}".format(x, y, z))
        logging.info('Price')
        logging.info(price)

        for name, price in zip(name_list, price):
            yield {'name': name,
                   'price/unit': price,
                   'category': category}
