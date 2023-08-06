from scrapy import signals
from urllib.parse import urlencode
from random import randint
import base64
import requests
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class DrogasilSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class DrogasilDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


# defining a middleware to call the fake headers API and generate fake headers for our requests
class FakeHeadersMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):

        self.api_key = settings.get('HEADER_GEN_API_KEY')
        self.endpoint = settings.get('HEADER_GEN_ENDPOINT',
                                               'https://headers.scrapeops.io/v1/browser-headers')
        self.is_active = settings.get('HEADER_GEN_IS_ACTIVE', False)
        self.num_results = settings.get('HEADER_GEN_NUM_RESULTS')
        self.headers = []
        self._get_user_agents_list()
        self._fake_headers_enabled()

    def _get_user_agents_list(self):

        payload = {
            'api_key': self.api_key
        }

        if self.num_results is not None:
            payload['num_headers'] = self.num_results

        response = requests.get(self.endpoint, params = urlencode(payload))
        json_data = response.json()
        self.headers = json_data.get('result', [])

    def _get_random_header(self):

        rand_index = randint(0, len(self.headers) - 1)
        return self.headers[rand_index]

    def _fake_headers_enabled(self):

        if self.api_key is None or self.api_key == "":
            self.is_active = False
        else:
            self.is_active = True

    def process_request(self, request, spider):

        rand_header = self._get_random_header()

        request.headers['user-agent'] = rand_header['user-agent']
        request.headers['accept-language'] = rand_header['accept-language']
        request.headers['accept-encoding'] = rand_header['accept-encoding']
        request.headers['sec-fetch-user'] = rand_header['sec-fetch-user']
        request.headers['sec-fetch-mod'] = rand_header['sec-fetch-mod']
        request.headers['sec-fetch-site'] = rand_header['sec-fetch-site']
        request.headers['sec-ch-ua-platform'] = rand_header['sec-ch-ua-platform']
        request.headers['sec-ch-ua-mobile'] = rand_header['sec-ch-ua-mobile']
        request.headers['sec-ch-ua'] = rand_header['sec-ch-ua']
        request.headers['accept'] = rand_header['accept']