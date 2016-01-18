__author__ = 'jaywinhuang'

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tencent_job.items import TencentJobItem
import re
from scrapy import log

class TencentJobSpider(CrawlSpider):
    log.msg('start crawl')
    name = 'tencentjob'
    allowed_domains = ['tencent.com']
    start_urls = ['http://hr.tencent.com/position.php']
    rules = [
        Rule(LinkExtractor(allow=(r'&start=\d{,2}')),follow=True,callback='parse_table'),
    ]
    # &start=\d{,1}
    print rules

    def parse_table(self,response):
        log.msg('start parse table !!!!!!!!!!!!!')
        for href in response.xpath(r'//*[@id="position"]/div[1]/table/tr/td[1]/a/@href').extract():
            item = TencentJobItem()
            item['issue_time'] = response.xpath(r'//*[@id="position"]/div[1]/table/tr[2]/td[5]/text()').extract()[0]
            yield scrapy.Request( 'http://hr.tencent.com/' + href,meta={'item':item},callback=self.parse_detail)

    def parse_detail(self,response):
        log.msg('detail parsing~~~~~~~~~~~ ')
        item = response.meta['item']
        item['company'] = 'tencent'
        item['title'] = response.xpath(r'//*[@id="sharetitle"]/text()').extract()[0]
        item['link'] = response.url
        item['id'] = re.findall(r'(\d+)',response.url)[0]
        item['location'] = response.xpath(r'//*[@id="position_detail"]/div/table/tr[2]/td[1]/text()').extract()[0]
        item['category'] = response.xpath(r'//*[@id="position_detail"]/div/table/tr[2]/td[2]/text()').extract()[0]
        duty = response.xpath(r'//*[@id="position_detail"]/div/table/tr[3]/td/ul/li').extract()
        item['duty'] = "".join(duty)
        requirement = response.xpath(r'//*[@id="position_detail"]/div/table/tr[4]/td/ul/li').extract()
        item['requirement'] = "".join(requirement)

        yield item




