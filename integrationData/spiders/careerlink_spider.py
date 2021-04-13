import scrapy
from integrationData.items import CareerlinkItem
from scrapy.loader import ItemLoader
import logging

class CareerlinkSpider(scrapy.Spider):
    name = "careerlink"
    count = 0
    home = 'https://www.careerlink.vn'
    def start_requests(self):
        urls = [
            'https://www.careerlink.vn/vieclam/list?category_ids=130%2C19&page=2'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        from scrapy.utils.response import open_in_browser
        open_in_browser(response)
        for job in response.xpath("//a[@class='job-link clickable-outside']"):
            job_url = job.xpath("@href").extract()
            print(self.home + job_url[0])
            if len(job_url) > 0:
                yield scrapy.Request(self.home + job_url[0], callback=self.parse_job)
        

        # self.count +=1 
        # next page
        next_page = response.xpath('//nav/ul/li/a[@rel="next" and @class="page-link d-none d-md-block"]/@href').extract()[0]
        print(next_page)
        if next_page is not None:
            next_page = self.home + next_page
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_job(self, response):
        newItem = ItemLoader(item=CareerlinkItem(), selector=response)
        #title
        newItem.add_xpath('title', '//h1[@itemprop="title"]/text()')
        #nameCompany
        newItem.add_xpath('nameCompany', "//p[@class='org-name mb-2']//span/text()")
        #salary
        newItem.add_xpath('salary', '//span[@itemprop="value"]/text()')
        #description
        newItem.add_xpath('description', '//div[@itemprop="description"]/p/text()')
        # requirement
        newItem.add_xpath('requirement', '//div[@itemprop="skills"]/p/text()')
        # employmentType
        newItem.add_xpath('employmentType', '//div[@itemprop="employmentType"]/text()')
        # qualifications
        newItem.add_xpath('qualifications', '//div[@itemprop="qualifications"]/text()')
        # experience
        newItem.add_xpath('experience', '//div[@itemprop="experienceRequirements"]/text()')
        # education
        newItem.add_xpath('education', '//div[@itemprop="educationRequirements"]/text()')
        #sex
        # newItem.add_xpath('experience', '//div[@itemprop="experienceRequirements"]/p/text()')
        #field
        newItem.add_xpath('field', '//span[@itemprop="occupationalCategory"]/text()')
        #address 
        newItem.add_xpath('address', '//div[@class="mb-1 text-body"]//span/text()')
        #updateDate
        newItem.add_xpath('updateDate', '//span[@itemprop="datePosted"]/text()')
        #deadline
        newItem.add_xpath('deadline', '//span[@itemprop="validThrough"]/text()')

        logging.info("Crawling ")
        yield newItem.load_item()

        
        


