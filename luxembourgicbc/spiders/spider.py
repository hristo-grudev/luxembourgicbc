import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import LuxembourgicbcItem
from itemloaders.processors import TakeFirst


class LuxembourgicbcSpider(scrapy.Spider):
	name = 'luxembourgicbc'
	start_urls = ['http://luxembourg.icbc.com.cn/ICBC/%E6%B5%B7%E5%A4%96%E5%88%86%E8%A1%8C/%E5%8D%A2%E6%A3%AE%E5%A0%A1%E5%88%86%E8%A1%8C%E7%BD%91%E7%AB%99/cn/%E5%85%B3%E4%BA%8E%E6%88%91%E8%A1%8C/%E5%B7%A5%E8%A1%8C%E6%96%B0%E9%97%BB/default.htm']

	def parse(self, response):
		post_links = response.xpath('//span[@class="ChannelSummaryList-insty"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@align="right"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//div[@class="TextTitle_style"]/span/text()').get()
		description = response.xpath('//td[@id="mypagehtmlcontent"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@id="InfoPickFromFieldControl"]/text()').get()
		if date:
			date = re.findall(r'\d+-\d+-\d+', date)[0]

		item = ItemLoader(item=LuxembourgicbcItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
