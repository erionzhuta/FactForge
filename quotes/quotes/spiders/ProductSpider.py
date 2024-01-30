import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from quotes.items import ProductItem


class ProductSpider(CrawlSpider):
    name = "Product"
    allowed_domains = ["setec.mk"]
    start_urls = [
        "https://setec.mk/index.php?route=product/category&path=10019_10020_10025&limit=31"
    ]

    rules = (Rule(LinkExtractor(allow=(
        "index.php?route=product/category&path=10019_10020_10025&limit=31")),
                  callback="parse_item",
                  follow=True), )

    def parse_item(self, response):
        Product = ProductItem()
        columns = response.css(
            '#mfilter-content-container > div.product-grid.active > div')

        for column in columns:
            rows = column.css('div')
            for row in rows:
                Product['name'] = row.css('div.name > a::text').extract_first()
                Product['price'] = row.css('div.price::text').extract_first()
                Product['link'] = row.css(
                    'div.name > a::attr(href)').extract_first()
                yield Product

        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        return


#mfilter-content-container > div.product-grid.active
#mfilter-content-container > div.product-grid.active > div:nth-child(1) > div:nth-child(1) > div
