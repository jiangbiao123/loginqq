# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule  # 提取超链接规则
from zhonghuakejiwang.items import ZhonghuakejiwangItem
from scrapy.linkextractors import LinkExtractor # 提取链接
from lxml import etree


class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['https://tech.china.com/articles/index.html']
    rules = (
        Rule(LinkExtractor(allow="article\\/.*?\\.html", restrict_xpaths='//*[@id="left_side"]/div[@class="con_item"]'),# allow主要作用是匹配的，restrict_xpath作用匹配的
             follow=True, callback="process_content"),
        Rule(LinkExtractor(allow="index_.*.html", restrict_xpaths='//*[@id="pageStyle"]/a'), follow=True),# 先用restrict_xpath做定位，然后allow再匹配更加精准一些
    )

    def process_content(self, response):
        item = ZhonghuakejiwangItem()
        item['title'] = response.xpath('//*[@id="chan_newsTitle"]/text()').extract()
        item['content'] = response.xpath('//*[@id="chan_newsDetail"]/p/text()').extract()
        item['url'] = response.url
        # item['time'] = response.xpath('//*[@id="chan_newsInfo"]/text()').re_first('(/d+-/d+-/d+/s/d+:/d+:/d+)')[0]
        # item['source'] = response.xpath('//*[@id="chan_newsInfo"]/text()').re_first('来源:(.*)').strip()
        print(item)
        yield item


    # def parse(self, response):
    #     # print(response.text)
    #     pass
