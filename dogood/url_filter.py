import random


class URLFilter:

    def __init__(self, urls, maximum=None):
        self.urls = set(urls)
        self.maximum = maximum

    def remove(self, urls_to_remove):
        filtered_urls = list(self.urls - set(urls_to_remove))
        maximum = self.maximum or len(filtered_urls)
        self.urls = set()
        for _ in range(maximum):
            url = random.choice(filtered_urls)
            self.urls.add(url)
            filtered_urls.remove(url)
