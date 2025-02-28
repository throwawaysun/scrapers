import re
import scrapy
from tpdb.BaseSceneScraper import BaseSceneScraper


class SiteAngelaWhiteScenesSpider(BaseSceneScraper):
    name = 'AngelaWhiteScenes'
    network = 'Angela White'
    parent = 'Angela White'
    site = 'Angela White'

    start_urls = [
        '',
    ]

    selector_map = {
        'title': '//h1[@class="description"]/text()',
        'description': '//h1[@class="description"]/following-sibling::p[1]//text()',
        'date': '//span[contains(text(), "eleased:")]/following-sibling::text()',
        'date_formats': ['%b %d, %Y'],
        'image': '//meta[@property="og:image"]/@content',
        'tags': '',
        'duration': '',
        'trailer': '',
        'external_id': r'/(\d+)/',
        'type': 'Scene',
    }

    def start_requests(self):
        meta = {}
        meta['page'] = 1
        link = 'https://angelawhitestore.com/94055/studio/agw-entertainment-porn-movies.html'
        yield scrapy.Request(link, callback=self.get_movies, meta=meta, headers=self.headers, cookies=self.cookies)

    def get_movies(self, response):
        movies = response.xpath('//a[@class="boxcover"]/@href').getall()
        for movie in movies:
            yield scrapy.Request(url=self.format_link(response, movie), callback=self.get_scenes)

    def get_scenes(self, response):
        meta = response.meta
        meta['dvdtitle'] = self.cleanup_title(response.xpath('//h1[@class="description"]/text()').get().strip())
        scenes = response.xpath('//div[contains(@class,"item-grid-scene")]/div[@class="grid-item"]/article')
        for scene in scenes:
            image = scene.xpath('.//a[@class="scene-img"]/img/@data-src')
            if image:
                meta['image'] = image.get()
                meta['image_blob'] = self.get_image_blob_from_link(meta['image'])
            performers = scene.xpath('.//p[contains(@class, "performer-names")]/a/text()')
            if performers:
                meta['performers'] = performers.getall()
            scene = scene.xpath('./div/a/@href').get()
            if re.search(self.get_selector_map('external_id'), scene):
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene, meta=meta)

    def get_duration(self, response):
        duration = response.xpath('//span[contains(text(), "ength:")]/following-sibling::text()')
        if duration:
            duration = duration.get()
            duration = re.search(r'(\d+) min', duration)
            if duration:
                return str(int(duration.group(1)) * 60)

    def get_title(self, response):
        meta = response.meta
        title = super().get_title(response)
        if "scene " in title.lower():
            title = meta['dvdtitle'] + " - " + title
        return title
