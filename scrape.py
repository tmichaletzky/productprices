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
        properties = response.xpath("//dt[@class='property-group__name']").getall()
        properties = list(map(
            lambda s: re.findall('property-group__name">\n(.*) </dt>', s)[0],
            properties
        ))
        values = response.xpath("//dd[@class='property-group__values']").getall()
        values = list(map(
            lambda s: re.findall('property-group__values">\n<span class="value">(.*)</span>', s)[0],
            values
        ))
        retval = {}
        for key,value in zip(properties, values):
            retval[key] = value
        return retval


