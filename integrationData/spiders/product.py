import scrapy
import requests
import base64
import logging
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader
from tutorial.items import FbcrawlItem, parse_date, parse_date2
from datetime import datetime
import os
from scrapy.utils.response import open_in_browser


def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)

class FacebookSpider(scrapy.Spider):
    name = "test"
    rotate_user_agent=True
    def __init__(self, **kwargs):
        super(FacebookSpider, self).__init__(**kwargs)

        # self.driver = webdriver.Chrome(executable_path='/Volumes/HHD/tutorial/tutorial/spiders/chromedriver')
        self.k = datetime.now().year
        self.max = 10000
        self.date = datetime(2020, 1, 1)
        self.max_date = datetime(2020, 8, 2)
        self.year = self.date.year
        self.count = 0
        self.last_page = list()
        self.filename = "last_page_" + str(kwargs['id']) + ".txt"
        self.group_id = ["281625105687554", "261857314290780", "721777084598266", "158251541614165", "2089095837981438"]
        if 'date' in kwargs:
            temp_url = "https://mbasic.facebook.com/groups/" + self.group_id[int(kwargs['id'])] + "?bac=" + kwargs['date']
            self.start_urls = [temp_url]
        else:
            with open(self.filename) as f:
                for last_line in f:
                    pass
            self.start_urls = [last_line]

    def parse(self, response):
        if not self.count:
            open_in_browser(response)
        # print("Parse_page")
        # print(response.xpath("//article[contains(@data-ft,'top_level_post_id')]"))
        for post in response.xpath("//article[contains(@data-ft,'top_level_post_id')]"):
            # print(post)
            many_features = post.xpath('./@data-ft').get()
            date = []
            date.append(many_features)
            date = parse_date(date)
            current_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') if date is not None else date
            if current_date is None:
                date_string = post.xpath('.//abbr/text()').get()
                date = parse_date2([date_string])
                current_date = datetime(date.year, date.month, date.day) if date is not None else date
                date = str(date)

            if self.date > current_date:  #or current_date > self.max_date:
                # raise CloseSpider('Reached date: {}'.format(self.date))
                continue

            new = ItemLoader(item=FbcrawlItem(), selector=post)
            if abs(self.count) + 1 > self.max:
                os.system('say Crawling is finished!')
                with open(self.filename, 'a') as f:
                    f.write("\n" + self.last_page[-2])
                open_in_browser(response)
                raise CloseSpider('Reached max num of post: {}. Crawling finished'.format(abs(self.count)))
            self.logger.info('Parsing post n = {}, post_date = {}'.format(abs(self.count) + 1, date))
            # new.add_xpath('comments', './footer/div[2]/a[1]/text()')
            new.add_value('a_date', date)
            new.add_xpath('a_post_id', './@data-ft')
            new.add_xpath('b_url', ".//a[contains(@href,'footer')]/@href")
            full_story = post.xpath(".//a[contains(@href,'footer')]/@href").extract()
            temp_post = response.urljoin(full_story[0])
            self.count -= 1
            # next_post = 'http://api.scraperapi.com/?api_key=' + API_KEY + '&url=' + temp_post + '&render=true'
            yield scrapy.Request(temp_post, self.parse_post, priority=self.count, meta={'item': new})
        # load next posts
        new_page = response.xpath("//div[contains(@id,'stories_container')]/div/a/@href").extract()
        # print(new_page)
        if not new_page:
            self.logger.info('[!] "more" link not found, will look for a "year" link')
            # self.k is the year link that we look for
            if response.meta['flag'] == self.k and self.k >= self.year:
                xpath = "//div/a[contains(@href,'time') and contains(text(),'" + str(self.k) + "')]/@href"
                new_page = response.xpath(xpath).extract()
                if new_page:
                    new_page = response.urljoin(new_page[0])
                    self.k -= 1
                    self.logger.info('Found a link for year "{}", new_page = {}'.format(self.k,new_page))
                    # next_page = 'http://api.scraperapi.com/?api_key=' + API_KEY + '&url=' + new_page + '&render=true'
                    yield scrapy.Request(new_page, callback=self.parse, meta={'flag':self.k})
                else:
                    while not new_page: #sometimes the years are skipped this handles small year gaps
                        self.logger.info('Link not found for year {}, trying with previous year {}'.format(self.k,self.k-1))
                        self.k -= 1
                        if self.k < self.year:
                            os.system('say Crawling is finished!')
                            with open(self.filename, 'a') as f:
                                f.write("\n" + self.last_page[-2])
                            open_in_browser(response)
                            raise CloseSpider('Reached date: {}. Crawling finished'.format(self.date))
                        xpath = "//div/a[contains(@href,'time') and contains(text(),'" + str(self.k) + "')]/@href"
                        new_page = response.xpath(xpath).extract()
                    self.logger.info('Found a link for year "{}", new_page = {}'.format(self.k,new_page))
                    new_page = response.urljoin(new_page[0])
                    # next_page = 'http://api.scraperapi.com/?api_key=' + API_KEY + '&url=' + new_page + '&render=true'
                    self.k -= 1
                    yield scrapy.Request(new_page, callback=self.parse, meta={'flag': self.k})
            else:
                os.system('say Crawling is finished!')
                self.logger.info('Crawling has finished with no errors!')
        else:
            new_page = response.urljoin(new_page[0])
            # next_page = 'http://api.scraperapi.com/?api_key=' + API_KEY + '&url=' + new_page + '&render=true'
            self.last_page.append(new_page)
            if 'flag' in response.meta:
                self.logger.info('Page scraped, clicking on "more"! new_page = {}'.format(new_page))
                yield scrapy.Request(new_page, callback=self.parse, meta={'flag': response.meta['flag']})
            else:
                self.logger.info('First page scraped, clicking on "more"! new_page = {}'.format(new_page))
                yield scrapy.Request(new_page, callback=self.parse, meta={'flag': self.k})

    def parse_post(self, response):
        # from scrapy.utils.response import open_in_browser
        # if abs(self.count) < 5:
        #     open_in_browser(response)
        new = ItemLoader(item=FbcrawlItem(), response=response, parent=response.meta['item'])
        new.add_xpath('a_source',
                      "//td/div/h3/strong/a/text() | //span/strong/a/text() | //div/div/div/a[contains(@href,'post_id')]/strong/text()")
        # new.add_xpath('shared_from',
        #               '//div[contains(@data-ft,"top_level_post_id") and contains(@data-ft,\'"isShare":1\')]/div/div[3]//strong/a/text()')
        #   new.add_xpath('date','//div/div/abbr/text()')
        new.add_xpath('a_text', '//div[@data-ft]//p//text() | //div[@data-ft]/p/text() | //div[@data-ft]/div[@class]/div[@class]/text() | //div[@data-ft]/div[@class]/div[@class]/div[@class]/span[@style]/text()')
        # crawl image
        image_source = response.xpath("//div[contains(@data-ft, 'top_level_post_id')]//a[contains(@href, 'photo')]/img/@src")
        encodes = list()
        for src in image_source.getall():
            code = get_as_base64(src)
            uri = ("data:" +
                   'image/jpeg' + ";" +
                   "base64," + code.decode("utf-8"))
            encodes.append(uri)
        new.add_value('pictures', encodes)
        yield new.load_item()

    def parse_comment(self, response):
        # from scrapy.utils.response import open_in_browser
        # open_in_browser(response)
        # load regular comments
        print("Parse comment")
        path2 = './/div[string-length(@class) = 2 and count(@id)=1 and contains("0123456789", substring(@id,1,1)) and not(.//div[contains(@id,"comment_replies")])]'
        for i, reply in enumerate(response.xpath(path2)):
            self.logger.info('{} regular comment'.format(i + 1))
            new = ItemLoader(item=FbcrawlItem(), selector=reply)
            new.add_xpath('source', './/h3/a/text()')
            new.add_xpath('post_id', '/div/@id')
            new.add_xpath('url', './/h3/a/@href')
            new.add_xpath('text', './/div[h3]/div[1]//text()')
            temp_date = reply.xpath('.//abbr/text()').get()
            date = parse_date2([temp_date])
            print(date)
            # current_date = datetime(date.year, date.month, date.day) if date is not None else date
            date = str(date)
            new.add_value('date', date)
            new.add_xpath('is_comment', '1')
            yield new.load_item()

        # new comment page
        prev_xpath = response.xpath('.//div[contains(@id,"see_prev")]/a/@href').extract()
        if prev_xpath is not None:
            temp_comment = response.urljoin(prev_xpath[0])
            yield scrapy.Request(temp_comment, self.parse_comment, priority=self.count)



