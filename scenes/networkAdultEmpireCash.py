import re
import scrapy
from tpdb.BaseSceneScraper import BaseSceneScraper


class AdultEmpireCashScraper(BaseSceneScraper):
    name = 'AdultEmpireCash'
    network = 'AdultEmpireCash'

    custom_settings = {'AUTOTHROTTLE_ENABLED': 'True', 'AUTOTHROTTLE_DEBUG': 'False', 'CONCURRENT_REQUESTS': '1'}

    start_urls = [
        # 'https://www.mypervyfamily.com/',  # Moved to AdulttimeAPI scraper
        'https://www.conorcoxxx.com',
        'https://www.hornyhousehold.com',
        'https://jayspov.net',
        # 'https://www.filthykings.com/',  # Moved to AdulttimeAPI scraper
        'https://thirdworldxxx.com',
        'https://latinoguysporn.com',
        'https://cospimps.com',
        'https://www.jonathanjordanxxx.com',
        'https://www.kingsoffetish.com',
        'https://pmggirls.com',
        'https://www.lethalhardcore.com',
        'https://www.smutfactor.com/',
        'https://spankmonster.com',
        'https://www.stephousexxx.com',
        'https://www.wcpclub.com'
        'https://www.bruthasinc.com'
    ]

    selector_map = {
        'title': '//h1[@class="description"]/text()',
        'description': '//div[@class="synopsis"]/p/text()',
        'date': '//div[@class="release-date"][1]/text()',
        'image': '//meta[@property="og:image"]/@content',
        'performers': '//div[@class="video-performer"]//img/@title',
        'tags': '//div[@class="tags"]//a/text()',
        'external_id': '(\\d+)/(.+)\\.html',
        'trailer': '',
        'pagination': '/watch-newest-clips-and-scenes.html?page=%s&hybridview=member'
    }

    def get_scenes(self, response):
        if "spankmonster" in response.url:
            scenes = response.xpath('//a[@class="grid-item-details"]/@href').getall()
            for scene in scenes:
                meta = {}
                meta['site'] = "Spank Monster"
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene, meta=meta)
        elif "stephousexxx" in response.url:
            scenes = response.xpath('//div[@class="animated-screenshot-container"]/a/@href').getall()
            for scene in scenes:
                meta = {}
                meta['site'] = "Stephouse XXX"
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene, meta=meta)
        elif "kingsoffetish" in response.url:
            scenes = response.xpath('//div[@class="animated-screenshot-container"]/a/@href').getall()
            for scene in scenes:
                meta = {}
                meta['site'] = "Kings of Fetish"
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene, meta=meta)
        elif "bruthasinc" in response.url:
            scenes = response.xpath('//div[@class="animated-screenshot-container"]/a/@href').getall()
            for scene in scenes:
                meta = {}
                meta['site'] = "Brutha's Inc"
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene, meta=meta)
        elif "jayspov" in response.url:
            scenes = response.xpath('//a[contains(@class, "scene-update-details")]/@href').getall()
            for scene in scenes:
                meta = {}
                meta['site'] = "Jays POV"
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene, meta=meta)
        elif "jonathanjordanxxx" in response.url:
            scenes = response.xpath('//div[@class="animated-screenshot-container"]/a/@href').getall()
            for scene in scenes:
                meta = {}
                meta['site'] = "Jonathan Jordan XXX"
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene, meta=meta)
        elif "latinoguys" in response.url:
            scenes = response.xpath('//div[@class="animated-screenshot-container"]/a/@href').getall()
            for scene in scenes:
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene)
        else:
            scenes = response.css('.grid-item')
            for scene in scenes:
                link = scene.css('a.grid-item-title::attr(href)').get()
                meta = {}
                if scene.css('p>span::text').get():
                    text = scene.css('p>span::text').get().strip().split('|')
                    if len(text) == 2:
                        meta['site'] = text[0].strip()
                yield scrapy.Request(url=self.format_link(response, link), callback=self.parse_scene, meta=meta)

    def get_site(self, response):
        if 'jayspov' in response.url:
            return 'Jays POV'
        if 'smutfactor' in response.url:
            return 'Smut Factor'
        if 'wcpclub' in response.url:
            return 'West Coast Productions'

        return response.xpath('//div[@class="studio"]//span[2]/text()').get().strip()

    def get_parent(self, response):
        if 'jayspov' in response.url:
            return 'Jays POV'
        if 'smutfactor' in response.url:
            return 'Smut Factor'
        if 'wcpclub' in response.url:
            return 'West Coast Productions'

        return response.xpath('//div[@class="studio"]//span[2]/text()').get().strip()

    def get_next_page_url(self, base, page):
        pagination = self.get_selector_map('pagination')

        if "conorcoxxx" in base:
            pagination = "/conor-coxxx-clips.html?page=%s&hybridview=member"
        if "hornyhousehold" in base:
            pagination = "/watch-newest-clips-and-scenes.html?page=%s&hybridview=member"
        if "jayspov" in base:
            pagination = "/jays-pov-updates.html?page=%s&hybridview=member"
        if "latinoguys" in base:
            pagination = "/watch-newest-latino-guys-porn-clips-and-scenes.html?page=%s&hybridview=member"
        if "cospimps" in base:
            pagination = "/videos/videos_page=%s"
        if "filthykings" in base:
            pagination = "/en/videos/page/%s"
        if "pmggirls" in base:
            pagination = "/videos/videos_page=%s"
        if "lethalhardcore" in base:
            pagination = "/watch-lethal-hardcore-streaming-video-scenes.html?page=%s&hybridview=member"
        if "smutfactor" in base:
            pagination = "/watch-newest-smut-factor-clips-and-scenes.html?page=%s&hybridview=member"
        if "spankmonster" in base:
            pagination = "/spank-monster-updates.html?page=%s&hybridview=member"
        if "stephousexxx" in base:
            pagination = "/watch-newest-step-house-xxx-clips-and-scenes.html?page=%s&hybridview=member"
        if "jonathanjordanxxx" in base:
            pagination = "/watch-newest-jonathan-jordan-xxx-clips-and-scenes.html?page=%s&hybridview=member"
        if "kingsoffetish" in base:
            pagination = "/kings-of-fetish-newest-perverted-clips.html?page=%s&hybridview=member"
        if "bruthasinc" in base:
            pagination = "/watch-newest-bruthas-inc-clips-and-scenes.html?page=%s&hybridview=member"
        return self.format_url(base, pagination % page)

    def get_title(self, response):
        title = super().get_title(response)
        titlework = super().get_title(response)
        titlework = re.sub('[^a-zA-Z]', '', titlework)
        if titlework == "Scene":
            release = response.xpath('//a[contains(@class, "movie-title")]/text()')
            if release:
                release = release.get()
                title = title + " From " + release.strip()
        return title

    def get_duration(self, response):
        duration = response.xpath('//span[contains(text(), "Length")]/following-sibling::text()')
        if duration:
            duration = duration.get()
            if "min" in duration:
                duration = re.search(r'(\d+)', duration).group(1)
                duration = str(int(duration) * 60)
                return duration
        return None
