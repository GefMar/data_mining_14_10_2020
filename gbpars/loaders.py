import re
from scrapy import Selector
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader

from .items import YoulaAutoItem, HHVacancyItem


def search_author_id(itm):
    re_str = re.compile(r'youlaId%22%2C%22([0-9|a-zA-Z]+)%22%2C%22avatar')
    result = re.findall(re_str, itm)
    return result


def create_user_url(itm):
    base_url = "https://youla.ru/user/"
    result = base_url + itm
    return result


def get_specification(itm):
    tag = Selector(text=itm)
    return {tag.xpath('//div/div[1]/text()').get(): tag.xpath('//div/div[2]/text()').get() or tag.xpath(
        '//div/div[2]/a/text()').get()}


def get_specification_out(itms):
    result = {}
    for itm in itms:
        if None not in itm:
            result.update(itm)
    return result


def description_rwrite(items):
    return ''.join(items)


class YoulaAutoLoader(ItemLoader):
    default_item_class = YoulaAutoItem
    autor_in = MapCompose(search_author_id, create_user_url)
    autor_out = TakeFirst()
    title_out = TakeFirst()
    specifications_in = MapCompose(get_specification)
    specifications_out = get_specification_out
    url_out = TakeFirst()


class HHVacancyLoader(ItemLoader):
    default_item_class = HHVacancyItem
    title_out = TakeFirst()
    url_out = TakeFirst()
    description_in = ''.join
    description_out = TakeFirst()
    salary_in = ''.join
    salary_out = TakeFirst()
