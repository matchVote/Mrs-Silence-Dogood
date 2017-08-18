import pytest
import yaml

from feeder.adapters import NewsapiAdapter


class TestNewsapiAdapter:
    """Test cases for NewsapiAdapter."""

    @pytest.fixture
    def config(self):
        with open('config/sources.yml') as f:
            self.config = yaml.load(f)['apis'][0]

    @pytest.fixture(autouse=True)
    def adapter(self, config):
        self.adapter = NewsapiAdapter(self.config)

    @pytest.fixture(autouse=True)
    def article_response(self):
        self.article_response = {
            'url': 'http://www.abc.com',
            'title': 'Awesome article',
            'author': 'Jimmy Hoffa',
            'description': 'This one time at band camp...',
            'urlToImage': 'http://www.flickr.com/1',
            'publishedAt': '2017-08-17T21:54:17Z'
            }

    def test_map_converts_author_value_into_list(self):
        result = self.adapter.map(self.article_response)
        assert result['authors'] == ['Jimmy Hoffa']

    def test_map_converts_author_none_value_into_empty_list(self):
        self.article_response['author'] = None
        result = self.adapter.map(self.article_response)
        assert result['authors'] == []
