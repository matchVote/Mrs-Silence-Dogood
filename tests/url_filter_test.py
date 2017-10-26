import pytest

from dogood import URLFilter


@pytest.fixture
def remove_urls():
    return ['I once met a man', 'so I bit him']


@pytest.fixture
def test_urls():
    return [
        'these could be any string',
        'http://test.com/whats_the_deal_with_airplane_peanuts',
        'I once met a man',
        'who had not had a bite in weeks',
        'so I bit him',
        '$IOIOKMLKJLKJSOIJ',
        'hodor',
        ]


class TestURLFilter:

    def test_urls_returns_a_set(self, test_urls):
        url_filter = URLFilter(test_urls)
        assert set(test_urls) == url_filter.urls

    def test_remove_sets_a_subset_of_urls_based_on_maximum(self, test_urls, remove_urls):
        url_filter = URLFilter(test_urls, maximum=3)
        url_filter.remove(remove_urls)
        assert len(url_filter.urls) == 3

    def test_remove_sets_a_randomly_selected_set_of_urls(self, test_urls, remove_urls):
        url_filter = URLFilter(test_urls, maximum=3)
        url_filter.remove(remove_urls)
        first_set = url_filter.urls
        url_filter = URLFilter(test_urls, maximum=3)
        url_filter.remove(remove_urls)
        second_set = url_filter.urls
        assert first_set != second_set

    def test_remove_filters_out_given_urls(self, test_urls, remove_urls):
        expected_urls = {
            'these could be any string',
            'http://test.com/whats_the_deal_with_airplane_peanuts',
            'who had not had a bite in weeks',
            '$IOIOKMLKJLKJSOIJ',
            'hodor',
            }

        url_filter = URLFilter(test_urls)
        url_filter.remove(remove_urls)
        assert expected_urls == url_filter.urls

    def test_remove_sets_urls_as_empty_set_if_all_urls_are_removed(self, test_urls):
        url_filter = URLFilter(test_urls)
        url_filter.remove(test_urls)
        assert url_filter.urls == set()

    def test_calculate_article_count_returns_length_of_url_list_when_not_given_maximum(self, test_urls):
        url_filter = URLFilter(test_urls)
        count = url_filter.calculate_article_count(test_urls)
        assert count == 7

    def test_calculate_article_count_returns_length_of_url_list_when_list_is_less_than_max(self, test_urls):
        url_filter = URLFilter(test_urls, maximum=20)
        count = url_filter.calculate_article_count(test_urls)
        assert count == 7

    def test_calculate_article_count_returns_maximum_if_url_list_length_is_greater(self, test_urls):
        url_filter = URLFilter(test_urls, maximum=3)
        count = url_filter.calculate_article_count(test_urls)
        assert count == 3
