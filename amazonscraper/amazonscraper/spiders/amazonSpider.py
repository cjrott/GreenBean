import scrapy
from scrapy_splash import SplashRequest

class AmazonSpider(scrapy.Spider):
    name = 'peter'
    
    def start_requests(self):
        url = 'https://www.amazon.com/s?k=groceries&ref=nb_sb_noss_1'
        url2 = 'https://www.amazon.com/s?k=canned+goods&crid=1S5XPRPNRO8MK&sprefix=canned+goods%2Caps%2C115&ref=nb_sb_noss_2'
        yield SplashRequest(url=url, callback=self.parse)

    def parse(self, response):
        # Scrape product details
        products = response.css('div.puis-card-container.s-card-container')
        for product in products:
            name = product.css('h2 a span.a-size-base-plus.a-color-base.a-text-normal::text').get()
            price = product.css('span.a-price span.a-offscreen::text').get()

            yield {
                'name': name,
                'price': price
            }

        # Get the link to the next page and continue scraping
        next_page = response.css('a.s-pagination-item.s-pagination-button::attr(href)').get()

        if next_page:
            next_page_url = response.urljoin(next_page)
            yield SplashRequest(next_page_url, callback=self.parse)


            
            
