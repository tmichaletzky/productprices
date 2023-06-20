import scrapy
import re

class MySpider(scrapy.Spider):
    name = "my-spider"
    start_urls = ["https://euronics.hu/tv-audio-jatekkonzol/televiziok-es-tartozekok/televizio-led-tv-oled-tv-qled-tv-c1594343"]
    #allowed_domains = ['']

    def parse(self, response, **kwargs):
        PRODUCT_SELECTOR = 'div.product-card'
        NEXT_SELECTOR = '.next a::attr("href")'

        product_cards = response.css(PRODUCT_SELECTOR).getall()
        product_urls = map(
            lambda s: re.findall('class="product-card__name-link" href="(.*)" title=', s)[0],
            product_cards)
        for product_url in product_urls:
            #print(f"FOUND ANOTHER PRODUCT: {product_url}")
            yield scrapy.Request(response.urljoin(product_url), callback=self.productParser)

        next_page = response.css(NEXT_SELECTOR).extract_first()
        if next_page:
            #print(f"REDIRECTING TO NEXT PAGE: {next_page}")
            yield scrapy.Request(response.urljoin(next_page))

    def productParser(self, response):
        price = re.findall(
            'itemprop="price" content="(.*)"',
            response.xpath("//h4[@class='price__content price pull-right']").get()
        )[0]
        serialnumber = re.findall(
            '">(.*)</span>',
            response.xpath("//li[@class='product__header-right-info']/span").get()
        )[0]
        product = re.findall(
            'itemprop="name">\n(.*)</h1>',
            response.xpath("//h1[@class='main-title product__header-right-title']").get()
        )[0]
        properties = list(map(
            lambda s: re.findall('property-group__name">\n(.*) </dt>', s)[0],
            response.xpath("//dt[@class='property-group__name']").getall()
        ))
        values = list(map(
            lambda s: re.findall('property-group__values">\n<span class="value">(.*)</span>', s)[0],
            response.xpath("//dd[@class='property-group__values']").getall()
        ))

        item = {
            "product":product,
            "serialnumber":serialnumber,
            "price": price,
        }
        for key,value in zip(properties, values):
            item[key] = value
        yield item

from scrapy.crawler import CrawlerProcess

if __name__ == "__main__":
    c = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0',
        'DOWNLOAD_DELAY': 1,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'products.json',
    })

    c.crawl(MySpider)
    c.start()
