import random


class URLFilter:

    def __init__(self, urls, maximum=None):
        self.urls = set(urls)
        self.maximum = maximum

    def remove(self, urls_to_remove):
        filtered_urls = list(self.urls - set(urls_to_remove))
        self.urls = set()
        if filtered_urls:
            count = self.calculate_article_count(filtered_urls)
            for _ in range(count):
                url = random.choice(filtered_urls)
                self.urls.add(url)
                filtered_urls.remove(url)

    def calculate_article_count(self, urls):
        if not self.maximum or len(urls) < self.maximum:
            return len(urls)
        else:
            return self.maximum
