import scrapy


class MaximaSpider(scrapy.Spider):
    name = "maxima"
    start_urls = ['https://www.e-maxima.ee/Pages/']

    def parse(self, response):
        food_drink = "https://www.e-maxima.ee/Products/sook-ja-jook.aspx"
        yield response.follow(food_drink, self.parse_category)

    def parse_category(self, response):
        for href in response.xpath("//ul[@id='submenu']/li/a/@href"):
            yield response.follow(href, self.parse_entry)

    def parse_entry(self, response):

        def extract_with_xpath(query):
            return response.xpath(query).extract()

        name_list = extract_with_xpath('//h3/a[contains (@id, "ctl00_MainContent_lstProduct")]/text()')
        price_list = extract_with_xpath('//td/p[@class="guide"]/strong/text()')
        price_unit = extract_with_xpath("//p[@class='guide']/text()[contains (.,'(')]")
        category = extract_with_xpath("//div/h1/text()")

        for x, y, z in zip(name_list, price_list, price_unit):
            yield {'name': x,
                   'price': y,
                   'price/unit': z,
                   'category': category
                   }
