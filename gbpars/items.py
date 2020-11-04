# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GbparsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class YoulaAutoItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    img = scrapy.Field()
    url = scrapy.Field()
    specifications = scrapy.Field()
    autor = scrapy.Field()


class HHVacancyItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    description = scrapy.Field()
    skills = scrapy.Field()
    company_url = scrapy.Field()
