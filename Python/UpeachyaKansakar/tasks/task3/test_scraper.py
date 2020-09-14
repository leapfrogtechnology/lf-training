import pytest

from task3 import generate_url_with_pagination

@pytest.mark.task3
def test_generate_url():
    expected_result = [
        'https://www.opencodez.com/category/web-development',
        'https://www.opencodez.com/category/web-development/page/2',
        'https://www.opencodez.com/category/web-development/page/3'
    ]
    output = generate_url_with_pagination(3)
    assert expected_result == output
