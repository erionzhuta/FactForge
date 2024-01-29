import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from quotes.items import QuotesItem
import os
import re
import codecs


class Quotecrawler1Spider(CrawlSpider):
    txt = '.txt'  # file extension
    fn = 'quotes.toscrape'  # name of the file to be saved (File Name)
    dn = fn + '.com'  # the site it will scrape (Domain Name)

    name = "QuoteCrawler1"
    allowed_domains = [dn]
    start_urls = ['https://' + dn + '/page/1']

    rules = (Rule(LinkExtractor(restrict_css=('span.tag-item')),
                  callback="parse_page",
                  follow=True), )

    def writeTxt(self, q):
        with codecs.open(self.fn + self.txt, 'a+', encoding='utf-8') as f:
            f.write(q['quotes'] + '\r\n')
            f.write(q['author'] + '\r\n')
            f.write(q['tags'] + '\r\n\n')

    def extractData(self, response):
        q = QuotesItem()  # instantiate the QuotesItem class

        for quote in response.css('div.quote'):
            q['quotes'] = '"' + re.sub(
                r'[^\x00-\x7F]', r'',
                quote.css('span.text::text').extract_first()) + '"'
            q['author'] = quote.css('small.author::text').extract_first()
            q['tags'] = ' '.join(
                str(s) for s in quote.css('div.tags > a.tag::text').extract())

            self.writeTxt(q)

    def parse_page(self, response):
        self.extractData(response)
