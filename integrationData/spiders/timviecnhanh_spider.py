import scrapy
from integrationData.items import TimviecnhanhItem
from scrapy.loader import ItemLoader
import logging
import time 

class QuotesSpider(scrapy.Spider):
    name = "timviecnhanh"
    home = 'https://timviecnhanh.com'
    count = 1
    priority = 0
    root_page = 'https://timviecnhanh.com/vieclam/timkiem?q=&province_ids=&field_ids[]=8&action=search&page='
    lastPage = False
    def start_requests(self):
        urls = [
            'https://timviecnhanh.com/vieclam/timkiem?q=&province_ids=&field_ids[]=8&action=search&page=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # from scrapy.utils.response import open_in_browser
        # open_in_browser(response)
        print("At page " + response.url)
        jobs = response.xpath("//a[@class='title-job ']")
        print("There are ", len(jobs))
        if len(jobs) < 1:
            self.lastPage = True
        for job in jobs:
            job_url = job.xpath("@href").extract()
            # print(self.home + job_url[0])
            if len(job_url) > 0:
                self.priority -= 1
                with open("needCrawlTimviecnhanh.txt", 'a') as f:
                    f.write(self.home +job_url[0] + "\n")
                yield scrapy.Request(self.home + job_url[0], callback=self.parse_job, priority = self.priority)
        time.sleep(5)
        if not self.lastPage:
            self.count +=1 
            self.priority -= 1
            # next page
            try:
                next_page = self.root_page + str(self.count)
                print(next_page)
                yield scrapy.Request(next_page, callback=self.parse, priority = self.priority-10)
            except:
                print("Get last page")
                self.lastPage = True


    def parse_job(self, response):
        # from scrapy.utils.response import open_in_browser
        # open_in_browser(response)
        newItem = ItemLoader(item=TimviecnhanhItem(), selector=response)
        #title
        newItem.add_xpath('title', '//div[@class="header-job-info bg-white"]//span[@class="title"]/text()')
        #updateDate
        updateDate = response.xpath('//div[@class="jsx-1425348829"]/text()').extract()[0]
        newItem.add_value('updateDate', updateDate)
        #nameCompany
        newItem.add_xpath('nameCompany', '//article//h3[@class="jsx-1425348829 mb-0"]/a/text()')
        # for x in response.xpath('//li[@class="jsx-1425348829 mb-1"]/text()'):
        #     print(x.extract())
        # print(response.xpath('(//article//li[@class="jsx-1425348829 mb-1"])[5]/a/text()').extract())
        # salary
        newItem.add_xpath('salary', '(//article//li[@class="jsx-1425348829 mb-1"])[1]/text()')
        #experience
        newItem.add_xpath('experience', '(//article//li[@class="jsx-1425348829 mb-1"])[2]/text()')
        #degree
        newItem.add_xpath('degree', '(//article//li[@class="jsx-1425348829 mb-1"])[3]/text()')
        #city
        newItem.add_xpath('city', '(//article//li[@class="jsx-1425348829 mb-1"])[4]/a/text()')
        #field
        newItem.add_xpath('field', '(//article//li[@class="jsx-1425348829 mb-1"])[5]/a/text()')
        #number
        newItem.add_xpath('number', '(//article//li[@class="jsx-1425348829 mb-1"])[6]/text()')
        #sex
        newItem.add_xpath('sex', '(//article//li[@class="jsx-1425348829 mb-1"])[7]/text()')
        #natureOfWork
        newItem.add_xpath('natureOfWork', '(//article//li[@class="jsx-1425348829 mb-1"])[8]/text()')
        #formOfWork
        newItem.add_xpath('formOfWork', '(//article//li[@class="jsx-1425348829 mb-1"])[9]/text()')
        #probationaryPeriod
        newItem.add_xpath('probationaryPeriod', '(//article//li[@class="jsx-1425348829 mb-1"])[10]/text()')
        #description
        newItem.add_xpath('description', '(//article//table[@class="d-none d-md-table word-break"]//tr//td)[2]/p/text()')
        #requirement
        newItem.add_xpath('requirement', '(//article//table[@class="d-none d-md-table word-break"]//tr//td)[4]/p/text()')
        #benefit
        newItem.add_xpath('benefit', '(//article//table[@class="d-none d-md-table word-break"]//tr//td)[6]/p/text()')
        #deadline
        newItem.add_xpath('deadline', '(//article//table[@class="d-none d-md-table word-break"]//tr//td)[8]/b/text()')
        #contactPerson
        # dang loi 
        # for content in response.xpath('(//article//table[@class="d-none d-md-table word-break"]//tr//td)[4]'):
        #     print(content.xpath("//p/text()").extract())
        # print(response.xpath('/article/div[4]/div/table/tbody/tr[1]/td[2]/p').extract())
        # //article//table[@class="jsx-1312632293 width-100"]//td[@class="jsx-1312632293"])[1]
        # newItem.add_xpath('contactPerson', '(//article//table[@class="jsx-1312632293 width-100"]//tr//td)[2]/p/text()')
        
        #address
        newItem.add_xpath('address', '//article//span[@class="jsx-1425348829 d-none d-md-block"]/text()')
        logging.info("Crawled " + response.url)
        with open("crawledTimviecnhanh.txt", 'a') as f:
            f.write(response.url + "\n")
        yield newItem.load_item()
        


