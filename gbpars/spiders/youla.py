import re
import scrapy
from pymongo import MongoClient


class YoulaSpider(scrapy.Spider):
    name = 'youla'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']
    xpath = {
        'brands': '//div[@class="TransportMainFilters_brandsList__2tIkv"]//a[@class="blackLink"]/@href',
        'ads': '//div[@id="serp"]//article//a[@data-target="serp-snippet-title"]/@href',
        'pagination': '//div[contains(@class, "Paginator_block")]/a/@href',
    }
    db_client = MongoClient()

    def parse(self, response, **kwargs):
        for url in response.xpath(self.xpath['brands']):
            yield response.follow(url, callback=self.brand_parse)

    def brand_parse(self, response, **kwargs):
        for url in response.xpath(self.xpath['pagination']):
            yield response.follow(url, callback=self.brand_parse)

        for url in response.xpath(self.xpath['ads']):
            yield response.follow(url, callback=self.ads_parse)

    def ads_parse(self, response, **kwargs):
        specifications = {
            itm.xpath('div[1]/text()').get(): itm.xpath('div[2]/text()').get() or itm.xpath('div[2]/a/text()').get() for
            itm in response.xpath('//div[contains(@class, "AdvertCard_specs")]//div[contains(@class, "AdvertSpecs")]')
            if itm.xpath('div[1]/text()').get()}

        name = response.xpath('//div[contains(@class, "AdvertCard_advertTitle")]/text()').extract_first()
        images = response.xpath('//div[contains(@class, "PhotoGallery_block")]//img/@src').extract()
        autor = self.js_decoder_autor(response)
        # процедура соранения в БД
        collection = self.db_client['parse_10'][self.name]
        collection.insert_one(
            {'title': name,
             'img': images,
             'url': response.url,
             'specifications': specifications,
             'autor': autor,
             }
        )

    def js_decoder_autor(self, response):
        script = response.xpath('//script[contains(text(), "window.transitState =")]/text()').get()
        re_str = re.compile(r"youlaId%22%2C%22([0-9|a-zA-Z]+)%22%2C%22avatar")
        result = re.findall(re_str, script)
        return f'https://youla.ru/user/{result[0]}' if result else None
