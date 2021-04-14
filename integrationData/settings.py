# Scrapy settings for integrationData project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'integrationData'

SPIDER_MODULES = ['integrationData.spiders']
NEWSPIDER_MODULE = 'integrationData.spiders'

# HTTP_PROXY = 'http://127.0.0.1:8123'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'Mozilla/5.0 (X11; Linux i686; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Mozilla/5.0 (Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'
    
]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    # 'scraper.middlewares.RandomUserAgentMiddleware': 400,
    # 'scraper.middlewares.ProxyMiddleware': 410,
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = True 

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 4
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'integrationData.middlewares.IntegrationdataSpiderMiddleware': 543,
# }

# ROTATING_PROXY_LIST = [
#     '160.238.242.42:8080',
#     '54.36.15.34:3128',
#     '51.178.86.220:80',	
#     '139.99.105.185:80',
#     '185.74.39.152:41258',
#     '103.120.144.144:80',
#     '161.202.226.194:80',
#     '3.8.209.87:80'
# ]

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
#     'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'integrationData.pipelines.IntegrationdataPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


URLLENGTH_LIMIT = 99999
FEED_EXPORT_ENCODING = 'utf-8'
DUPEFILTER_DEBUG = True
LOG_LEVEL = 'INFO'
