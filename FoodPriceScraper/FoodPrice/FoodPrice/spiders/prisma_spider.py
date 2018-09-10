import logging

import scrapy
from scrapy_splash import SplashRequest


class PrismaSpider(scrapy.Spider):
    name = "prisma"
    start_urls = ['https://www.prismamarket.ee/']
    script1 = """
                function main(splash, args)
                assert (splash:go(args.url))
                assert (splash:wait(0.5))
                return {
                    html = splash: html(),
                    png = splash:png(),
                    har = splash:har(),
                }
                end
              """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        food_drink = "https://www.prismamarket.ee/products"
        yield SplashRequest(food_drink, self.parse_category, args={'wait': 0.5})

    def parse_category(self, response):
        for href in response.xpath("//a[@class='js-category-item']/@href"):
            yield SplashRequest(response.urljoin(href.extract()), self.parse_subcategory, args={'wait': 0.5})

    def parse_subcategory(self, response):

        for href in response.xpath("//a[@class='js-category-item']/@href"):
            yield SplashRequest(response.urljoin(href.extract()), self.parse_item, endpoint='execute',
                                args={
                                    'html': 1,
                                    'lua_source': self.script1,
                                    'wait': 0.5,
                                })

    def parse_item(self, response):
        name_list = response.xpath("//div[@class='info relative clear']/div[@class='name']/text()").extract()
        whole_list = response.xpath("//div[@class='js-info-price']/span[@class='whole-number ']/text()").extract()
        decimal_list = response.xpath("//div[@class='js-info-price']/span[@class='decimal']/text()").extract()
        unit_list = response.xpath("//div[@class='js-info-price']/span[@class='unit']/text()").extract()
        category = response.xpath("//h2[@class='js-products-page-name viewport category-header']/text()").extract()[0]

        logging.info(name_list)
        logging.info(len(name_list))
        logging.info(whole_list)
        logging.info(len(whole_list))
        logging.info(decimal_list)
        logging.info(len(decimal_list))
        logging.info(unit_list)
        logging.info(len(unit_list))

        filename = 'mywebsite-%s.html' % '1'
        with open(filename, 'wb') as f:
            f.write(response.body)

        price = []
        for x, y, z in zip(whole_list, decimal_list, unit_list):
            price.append("{}.{}{}".format(x, y, z))

        for name, price in zip(name_list, price):
            yield {'name': name,
                   'price/unit': price,
                   'category': category}
