# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline

class ChineseWordsPipeline(object):
    def process_item(self, item, spider):
        return item


class CustomPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print("---------------------")
        requests = []
        count = 0
        image_names = item.get("image_name")
        for x in item.get('image_urls', []):
            requests.append(Request(x, meta={'image_name': image_names[count]}))
            count +=1
        return requests
            
        #return [Request(x, meta={'image_name': item["image_name"]})
        #        for x in item.get('image_urls', [])]

    def file_path(self, request, response=None, info=None):
        return '%s.jpg' % request.meta['image_name']
    