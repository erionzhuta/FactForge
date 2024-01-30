#CSS selectors
id = response.css('#mora_da_ima_prazno_mesto > a::attr(href)').get()
name = response.css('#mora_da_ima_prazno_mesto > a::text').extract_first().strip()
regular_price =  response.css('div.category-price-redovna > span.price-old-new::text').get().strip()
club_price =  response.css('div.category-price-akciska > span.price-new-new::text').get().strip()
image = response.css('div.image > a > img::attr(data-echo)').get().strip()
available = response.css('div.lager > div.ima_zaliha::text').get()

next = #mfilter-content-container > div.row.pagination-results > div.col-sm-6.text-left > ul
#mfilter-content-container > div.row.pagination-results > div.col-sm-6.text-left > ul > li:nth-child(4) > a