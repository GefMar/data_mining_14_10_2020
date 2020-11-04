import re
import scrapy
from ..loaders import YoulaAutoLoader


class YoulaSpider(scrapy.Spider):
    name = 'youla'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']
    xpath = {
        'brands': '//div[@class="TransportMainFilters_brandsList__2tIkv"]//a[@class="blackLink"]/@href',
        'ads': '//div[@id="serp"]//article//a[@data-target="serp-snippet-title"]/@href',
        'pagination': '//div[contains(@class, "Paginator_block")]/a/@href',
    }

    def parse(self, response, **kwargs):
        test_item = {'data': ['hello']}
        for url in response.xpath(self.xpath['brands']):
            yield response.follow(url, callback=self.brand_parse, cb_kwargs={'test_item': test_item})

    def brand_parse(self, response, **kwargs):
        kwargs['test_item']['data'].append("brand_parse")
        for url in response.xpath(self.xpath['pagination']):
            yield response.follow(url, callback=self.brand_parse)

        for url in response.xpath(self.xpath['ads']):
            yield response.follow(url, callback=self.ads_parse, cb_kwargs=kwargs)

    def ads_parse(self, response, **kwargs):
        print(1)
        loader = YoulaAutoLoader(response=response)
        loader.add_xpath('title', '//div[contains(@class, "AdvertCard_advertTitle")]/text()')
        loader.add_xpath('img', '//div[contains(@class, "PhotoGallery_block")]//img/@src')
        loader.add_xpath('autor', '//script[contains(text(), "window.transitState =")]/text()')
        loader.add_xpath('specifications',
                         '//div[contains(@class, "AdvertCard_specs")]//div[contains(@class, "AdvertSpecs")]')
        loader.add_value('url', response.url)
        yield loader.load_item()
