import scrapy
from inclist.items import IngredientItem

class IncilistSpider(scrapy.Spider):
    name = "incilist"
    allowed_domains = ["renude.co"]
    start_urls = ["https://renude.co/ingredients"]

    def parse(self, response):
        # Extract ingredient links from the current page
        ingredient_links = response.css('a.flex.flex-col.gap-2::attr(href)').getall()
        
        # Follow each ingredient link
        for link in ingredient_links:
            yield response.follow(link, callback=self.parse_ingredient)

        # Handles pagination
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_ingredient(self, response):
        item = IngredientItem()
        
        item['name'] = response.css('h1.font-patron.text-3xl::text').get()
        item['scientific_name'] = response.css('p.font-brandford.text-lg i::text').get()
        item['short_description'] = response.css('p.font-brandford.text-lg.mx-5::text').get()
        item['what_is_it'] = response.xpath('//h2[contains(text(), "What is")]/following-sibling::p[1]/text()').get()
        item['what_does_it_do'] = response.xpath('//h2[contains(text(), "What does")]/following-sibling::p[1]/text()').get()
        item['who_is_it_good_for'] = response.xpath('//h2[contains(text(), "Who is")]/following-sibling::div//p/text()').getall()
        item['who_should_avoid'] = response.xpath('//h2[contains(text(), "Who should avoid")]/following-sibling::div//p/text()').getall()
        item['url'] = response.url

        yield item