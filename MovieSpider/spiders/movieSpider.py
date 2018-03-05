# -*- coding: utf-8 -*-
from MovieSpider.items import MoviespiderItem
from scrapy_redis.spiders import RedisSpider
from scrapy.conf import settings
import scrapy
import requests
import lxml.html

# def getEveryItem(url, response):
#     selector = lxml.html.document_fromstring(url)
#     movie_list_group = selector.xpath('//div[@class="info"]')
#     movieList = []
#     for eachMoive in movie_list_group:
#         item = MoviespiderItem()
#         item['movie_title'] = eachMoive.xpath('div[@class="hd"]/a/span[1]/text()')
#         item['movie_other_title'] = eachMoive.xpath('div[@class="hd"]/a/span[3]/text()')
#         item['movie_link'] = eachMoive.xpath('div[@class="hd"]/a/@href')[0]
#         item['movie_director_actor'] = eachMoive.xpath('div[@class="bd"]/p[@class=""]/text()')
#         item['movie_star'] = eachMoive.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[
#             0]
#         item['movie_quote'] = eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()')
#         print(item['movie_title'])
#         movieList.append(item)
#     return movieList
#
#
# def getSource(url):
#     head = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36'}
#     content = requests.get(url, headers=head)
#     content.encoding = 'utf-8'  # 强制修改编码,防止Windows下出现乱码
#     return content.content
#
# doubanUrl = 'https://movie.douban.com/top250?start={}&filter='


# class MoviespiderSpider(RedisSpider):
#     name = "movieSpider"
#     allowed_domains = ['movie.douban.com']
#     redis_key = 'movieSpider:start_urls'
# class MoviespiderSpider(scrapy.Spider):
#     name = 'movieSpider'
#     allowed_domains = ['movie.douban.com']
#     start_urls = ['http://movie.douban.com/subject/26861685/?from=showing']
#     urls = 'http://movie.douban.com/top250'
#
#     def parse(self, response):
#
#         movie_list_group = response.xpath('//div[@class="info"]')
#         for movie_list in movie_list_group:
#             item = MoviespiderItem()
#             item['movie_title'] = movie_list.xpath('div[@class="hd"]/a/span[1]/text()').extract()
#             item['movie_other_title'] = movie_list.xpath('div[@class="hd"]/a/span[3]/text()').extract()
#             item['movie_link'] = movie_list.xpath('div[@class="hd"]/a/@href')[0].extract()
#             item['movie_director_actor'] = movie_list.xpath('div[@class="bd"]/p[@class=""]/text()').extract()
#             item['movie_star'] = movie_list.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0].extract()
#             item['movie_quote'] = movie_list.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
#             # print("==================")
#             # print(pageLink)
#             pageLink = getSource(pageLink)
#             movieList += getEveryItem(pageLink, response)
#             yield scrapy.Request(pageLink, callback=self.parse_movie_list_detail, meta={'item': item})
#
#     def parse_movie_list_detail(self, response):
#         movie_list_group = response.xpath('//div[@class="info"]')
#         result = []
#         for eachMoive in movie_list_group:
#             item = response.meta['item']
#             item['movie_title'] = eachMoive.xpath('div[@class="hd"]/a/span[1]/text()').extract()
#             item['movie_other_title'] = eachMoive.xpath('div[@class="hd"]/a/span[3]/text()').extract()
#             item['movie_link'] = eachMoive.xpath('div[@class="hd"]/a/@href')[0].extract()
#             item['movie_director_actor'] = eachMoive.xpath('div[@class="bd"]/p[@class=""]/text()').extract()
#             item['movie_star'] = eachMoive.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0].extract()
#             item['movie_quote'] = eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
#             print(item)
#             result.append(item)
#
#         return  result

    # def parse(self, response):
    #
    #     # print(response.body.decode())
    #
    #     movieList = []
    #     for i in range(10):
    #         pageLink = doubanUrl.format(i * 25)
    #         # scrapy.Request(pageLink, callback=self.parse_movie_list_detail, meta={'item': item})
    #         # print("==================")
    #         # print(pageLink)
    #         pageLink = getSource(pageLink)
    #         movieList += getEveryItem(pageLink, response)
    #     return movieList

# class MoviespiderSpider(scrapy.Spider):
#     name = 'movie'
#     allowed_domains = ['movie.douban.com']
#     start_urls = ('https://movie.douban.com/top250?start=0&filter=',)


class ReadColorSpider(RedisSpider):
    name = "movie"
    allowed_domains = ['movie.douban.com']
    redis_key = 'start_urls'

    main_url = 'https://movie.douban.com/top250'

    def parse(self, response):

        movie_list_group = response.xpath('//div[@class="info"]')
        for movie_list in movie_list_group:
            item = MoviespiderItem()
            item['movie_title'] = movie_list.xpath('div[@class="hd"]/a/span[@class="title"]/text()').extract()
            item['movie_other_title'] = movie_list.xpath('div[@class="hd"]/a/span[@class="other"]/text()').extract()
            item['movie_link'] = movie_list.xpath('//div[@class="hd"]/a/@href')[0].extract()
            item['movie_director_actor'] = movie_list.xpath('div[@class="bd"]/p[@class=""]/text()').extract()
            item['movie_star'] = movie_list.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0].extract()
            item['movie_quote'] = movie_list.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            url = movie_list.xpath('//div[@class="hd"]/a/@href')[0].extract()
            yield scrapy.Request(url, callback=self.parse_movie_list_detail, dont_filter=True, meta={'item': item})

        next_page = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_page:
            print(next_page)
            yield scrapy.Request(self.main_url + next_page[0], callback=self.parse)
        # else:
        #     self.crawler.engine.close_spider('queue is empty, the spider close')

    def parse_movie_list_detail(self, response):
            item = response.meta['item']
            # print(item)
            yield item
