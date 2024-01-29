import scrapy
import os
import re
import codecs

from scrapy.http import Request
from quotes.items import QuotesItem


class QuotespiderSpider(scrapy.Spider):
    txt = '.txt'  # file extension
    all = False  # scrape all pages or just the first page
    # name of the file to be saved (File Name)
    fn = 'quotes.toscrape'
    # the site it will scrape (Domain Name)
    dn = fn + '.com'
    # first page to be scraped
    firstPage = ['https://' + dn + '/page/1/']
    scope = [  # the scope of the scraping when all is set to False
        'https://' + dn + '/page/1/',
        'https://' + dn + '/page/2/',
        'https://' + dn + '/page/3/',
        'https://' + dn + '/page/4/',
    ]
    name = "QuoteSpider"
    allowed_domains = [dn]
    start_urls = [dn]

    # the function that will be called when the spider is run so we get a fresh scrape
    def delFile(self):
        if os.path.exists(self.fn + self.txt):
            os.remove(self.fn + self.txt)
        else:
            print("The file does not exist")

    def start_requests(self):
        self.delFile()
        pages = self.firstPage if self.all else self.scope

        for page in pages:
            yield scrapy.Request(
                page, callback=self.parse
            )  # callback is the function that will be called after the request is made

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

    def parse(self, response):
        self.extractData(response)

    def writeTxt(self, q):
        with codecs.open(self.fn + self.txt, 'a+', encoding='utf-8') as f:
            f.write(q['quotes'] + '\r\n')
            f.write(q['author'] + '\r\n')
            f.write(q['tags'] + '\r\n\n')
