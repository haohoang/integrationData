# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TimviecnhanhItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    updateDate = scrapy.Field()
    nameCompany = scrapy.Field()
    salary = scrapy.Field()
    experience = scrapy.Field()
    degree = scrapy.Field()
    city = scrapy.Field()
    field = scrapy.Field()
    number = scrapy.Field()
    sex = scrapy.Field()
    natureOfWork = scrapy.Field()
    formOfWork = scrapy.Field()
    probationaryPeriod = scrapy.Field()
    description = scrapy.Field()
    requirement = scrapy.Field()
    benefit = scrapy.Field()
    deadline = scrapy.Field()
    # contactPerson = scrapy.Field()
    address = scrapy.Field()

class CareerlinkItem(scrapy.Item):
    title = scrapy.Field()
    nameCompany = scrapy.Field()
    salary = scrapy.Field()
    description = scrapy.Field()
    requirement = scrapy.Field()
    employmentType = scrapy.Field()
    qualifications = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    #sex = scrapy.Field()
    field = scrapy.Field()
    address  = scrapy.Field()
    updateDate = scrapy.Field()
    deadline = scrapy.Field()

class CareerbuilderItem(scrapy.Item):
    description = scrapy.Field()
    requirement = scrapy.Field()
    benefit = scrapy.Field()
    url = scrapy.Field()
    qualifications = scrapy.Field()
    salary = scrapy.Field()
    employmentType = scrapy.Field()
    updateDate = scrapy.Field()
    deadline = scrapy.Field()

