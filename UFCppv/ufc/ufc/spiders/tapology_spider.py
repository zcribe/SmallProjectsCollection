import scrapy


class TapologySpider(scrapy.Spider):
    name = 'tapology'
    '//table[@class="siteSearchResults"]/tr/td/a/@href'

    def start_requests(self):
        start_url = 'https://www.tapology.com/search/mma-event-figures/ppv-pay-per-view-buys-buyrate'
        yield scrapy.Request(url=start_url, callback=self.get_links)

    def get_links(self, response):
        links = response.xpath('//table[@class="siteSearchResults"]/tr/td/a/@href').extract()

        for url in links:
            yield scrapy.Request(url=('https://www.tapology.com/' + url), callback=self.parse)

    def error_correction(self, header_list: list, contents_list: list) -> tuple:

        def remove_artifacts(input: list) -> list:
            artifacts = ['|', '\n', '\\n']
            return [a for _ in input if a not in artifacts]

        def length_correction(a: list, b: list) -> tuple:
            print(list(zip(a, b)))
            if len(a) == len(b):
                return a, b

        length_correction(header_list, contents_list)

    def parse(self, response):
        card = {}
        event = {}
        counter = 0

        def extract_with_xpath(query):
            return response.xpath(query).extract()

        headers = extract_with_xpath('//div[@class="right"]/ul[@class="clearfix"]/li/strong/text()')
        contents = extract_with_xpath('//div[@class="right"]/ul[@class="clearfix"]/li/span/text()')

        headers, contets = self.error_correction(headers, contents)

        for header, content in zip(headers, contents):
            event[header] = content

        for bout in response.xpath('//li[@class="fightCard"]'):
            details = self.parse_bout(bout)
            card[counter] = details
            counter += 1

        event['card'] = card

        yield event

    def parse_bout(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract()

        result = extract_with_xpath('//span[@class="result"]/text()')
        time = extract_with_xpath('//span[@class="time"]/text()')
        fight_number = extract_with_xpath('//div[@class="fightCardBoutNumber"]/text()')
        winner = extract_with_xpath('//div[@class="fightCardFighterName left"]/a/text()')
        winner_record = extract_with_xpath(
            '//div[@class="fightCardFighterBout left win"]/div[@class="fightCardFighterRank"]/text()')
        loser = extract_with_xpath('//div[@class="fightCardFighterName right"]/a/text()')
        loser_record = extract_with_xpath(
            '//div[@class="fightCardFighterBout loss right"]/div[@class="fightCardFighterRank"]/text()')
        billing = extract_with_xpath('//span[@class="billing"]/a/text()')
        weight_class = extract_with_xpath('//span[@class="weight"]/text()')

        return {'result': result,
                'time': time,
                'fightNumber': fight_number,
                'winner': winner,
                'loser': loser,
                'winnerRecord': winner_record,
                'loserRecord': loser_record,
                'billing': billing,
                'weightClass': weight_class}


if __name__ == '__main__':
    a = TapologySpider()
    test2 = ['Pay Per View', '\n', '\n', 'Zuffa, LLC', 'MGM Grand Garden Arena', 'Octagon', 'Mike Goldberg, Joe Rogan',
             'Bruce Buffer', 'Joe Rogan', '$2,336,000', '13,520', '(Paid: 11,634)', '150,000', '|', '8']
    test1 = ['U.S. Broadcast:', 'Promotion:', 'Ownership:', 'Venue:', 'Location:', 'Enclosure:', 'TV Announcers:',
             'Ring Announcer:', 'Post-Fight Interviews:', 'Ticket Revenue (live gate):', 'Attendance:',
             'PPV Buys / Buyrate:', 'TV Ratings:', 'Number of MMA Bouts:', 'Promotion Links:', 'Event Links:']
    print(a.error_correction(test1, test2))
