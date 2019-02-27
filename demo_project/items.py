# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

def remove_quotations(value):

    return value.replace(u"\u201d",'').replace(u"\u201c",'')
 
class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field(
        input_processor = MapCompose(str.strip, remove_quotations),
        output_processor = TakeFirst()
    )
    author = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    tags = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = Join(',')
    )

def strip_commas(x):
    return x.strip(',')

class HouseItem(scrapy.Item):
    listPrice = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    salePrice = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    zipcode = scrapy.Field(
        input_processor = MapCompose(),
        output_processor = TakeFirst()
    )
    daysOnMarket = scrapy.Field(
        input_processor = MapCompose(remove_quotations),
        output_processor = TakeFirst()
    )
    area = scrapy.Field(
        input_processor = MapCompose(strip_commas),
        output_processor = TakeFirst()
    )
    beds = scrapy.Field(
        input_processor = MapCompose(remove_quotations),
        output_processor = TakeFirst()
    )
    baths = scrapy.Field(
        input_processor = MapCompose(remove_quotations),
        output_processor = TakeFirst()
    )
