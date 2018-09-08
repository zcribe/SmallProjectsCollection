import scrapy


class SelverSpider(scrapy.Spider):
    name = "selver"

    start_urls = ['https://www.selver.ee/']

    def parse(self, response):
        for href in response.xpath('//nav/ul/li/a/@href'):
            yield response.follow(href, self.parse_categories)

    def parse_categories(self, response):
        for href in response.xpath('//div/ol/li/a/@href'):
            yield response.follow(href, self.parse_entry)

        for href in response.xpath('//li/a[contains (@title, "Järgmine")]/@href'):
            yield response.follow(href, self.parse_categories)

    def parse_entry(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first()

        yield {'name': extract_with_xpath('//div/div/h1/text()'),
               'price': extract_with_xpath('//span[@itemprop="price"]/@content'),
               'price/unit': extract_with_xpath('//span[@class="unit-price"]/text()'),
               'barcode': extract_with_xpath('//tr/td/text()')
               }
