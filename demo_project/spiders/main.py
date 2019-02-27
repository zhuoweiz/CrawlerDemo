import scrapy
from scrapy.loader import ItemLoader
from demo_project.items import QuoteItem, HouseItem

class DemoSpider(scrapy.Spider):
	#identity
	name = "demo"
	
	#Request
	def start_requests(self):
		urls = []
		for zipcode in self.settings.get('ZIPCODE'):
			self.zipcode = zipcode
			urls.append('https://www.redfin.com/zipcode/' + zipcode + '/housing-market')

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	# start_urls = [
	# ]

	# Response
	def parse(self, response):
		for house in response.xpath("//div[@class='slider-item']"):

			houseLoader = ItemLoader(item=HouseItem(), selector=house, response=response)
			houseLoader.add_xpath('listPrice',".//div[@class='detail'][1]//span/text()")
			houseLoader.add_xpath('salePrice',".//span[contains(@class,'homecardPrice')]/text()")
			houseLoader.add_xpath('zipcode',self.zipcode)
			houseLoader.add_xpath('daysOnMarket',".//div[@class='detail'][3]//span/text()")
			houseLoader.add_xpath('area',".//div[contains(@class, 'HomeStats')]/div[3]/div[@class='value']/text()")
			houseLoader.add_xpath('beds',".//div[contains(@class, 'HomeStats')]/div[1]/div[@class='value']/text()")
			houseLoader.add_xpath('baths',".//div[contains(@class, 'HomeStats')]/div[2]/div[@class='value']/text()")

			yield houseLoader.load_item()
			# yield {
			# 	'listPrice' : house.xpath(".//div[@class='detail'][1]//span/text()").extract(),
			# 	'salePrice' : house.xpath(".//div[@class='detail'][2]//div[@class='value']/text()").extract(),
			# 	'daysOnMarket': house.xpath(".//div[@class='detail'][3]//span/text()").extract()
			# }

		# /quotes?page=2, more pages
		# next_page = response.selector.xpath("//a[@class='next_page']/@href").extract_first()
		# next_zipcode = self.zipcodes[self.counter+1]

		# if (next_page is not None) and next_page[len(next_page)-1] < '4':
		# 	next_page_link = response.urljoin(next_page)
		# 	print("========== Next page ============ %s",next_page[len(next_page)-1])
		# 	yield scrapy.Request(url = next_page_link, callback=self.parse)
