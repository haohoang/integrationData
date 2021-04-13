#password = "123456@123"

import scrapy
# from integrationData.items import CareerbuilderItem
# from scrapy.loader import ItemLoader
import logging
import re
import json
import time

class CareerlinkSpider(scrapy.Spider):
    name = "careerbuilder"
    count = 0
    lastPage = False 
    # home = 'https://careerbuilder.vn'
    def start_requests(self):
        urls = [
            'https://careerbuilder.vn/viec-lam/cntt-phan-cung-mang-cntt-phan-mem-c63,1-trang-3-vi.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # from scrapy.utils.response import open_in_browser
        # open_in_browser(response)
        time.sleep(5)
        print("At page " + response.url)
        jobs = response.xpath('//a[@class="job_link"]')
        print("There are ", len(jobs))
        if len(jobs) < 1:
            self.lastPage = True
        for job in jobs:
            job_url = job.xpath("@href").extract()
            # print(job_url)
            if len(job_url) > 0:
                # save link need to be crawled
                self.count -= 1
                with open("needCrawl.txt", 'a') as f:
                    f.write(job_url[0] + "\n")
                yield scrapy.Request(job_url[0], callback=self.parse_job, priority=self.count)
            
        time.sleep(5)
        if not self.lastPage:
            self.count -=1 
            # next page
            try:
                next_page = response.xpath('//li[@class="next-page"]/a/@href').extract()[0]
                # print(next_page)
                if next_page is not None:
                    # next_page = self.home + next_page
                    print("Next Page: " + next_page)
                    
                    yield scrapy.Request(next_page, callback=self.parse, priority=self.count-10)
            except:
                print("Get Last page")
                self.lastPage = True


    def parse_job(self, response):
        data = response.xpath('//script[@type="application/ld+json"]/text()').extract()[1]
        data = re.sub("&nbsp;", "", data)
        data = re.sub("<[^>]*>", "", data)
        data = re.sub("\r|\n|\t","", data)
        data = json.loads(data)
        data["url"] = response.url
        if len(response.xpath('//div[@class="info"]/p/text()').extract()) > 0:
            # print(response.xpath('//div[@class="info"]/p/text()').extract())
            data["jobLocation"]["address"]["detailAddress"] = response.xpath('//div[@class="info"]/p/text()').extract()[0]
            logging.info("Crawled " + response.url)
            # save link is crawled
            with open("crawled.txt", 'a') as f:
                f.write(response.url + "\n")
            yield data
        else:
            address_url = None
            try:
                address_url = response.xpath("//li[@id='tabs-job-company']/a/@href").extract()[0]
            except:
                try:
                    # template thay doi
                    address_url = response.xpath('//a[@class="company"]/@href').extract()[0]
                except:
                    # thong tin cua cong ty duoc bao mat
                    data["jobLocation"]["address"]["detailAddress"] = ""
                    with open("crawled.txt", 'a') as f:
                        f.write(response.url + "\n")
                    yield data
            # print(address_url)
            if address_url is not None:
                self.count -= 1
                yield scrapy.Request(address_url, callback=self.parse_company, priority = self.count, meta={'item': data})
    
    def parse_company(self, response):
        # print(response.xpath("//div[@class='content']/p/text()").extract())
        try:
            address = response.xpath("//div[@class='content']/p/text()").extract()[1]
        except:
            try:
                # template thay doi
                address = response.xpath('//p[@class="company-location"]/text()').extract()[0]
            except:

                address = ""

        data = response.meta['item']
        data["jobLocation"]["address"]["detailAddress"] = address
        logging.info("Crawled " + data["url"])
        with open("crawled.txt", 'a') as f:
            f.write(data['url'] + "\n")
        yield data



        
        


