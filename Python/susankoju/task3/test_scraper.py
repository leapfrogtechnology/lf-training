''' Test file for scraper.py '''
import pytest
from bs4 import BeautifulSoup

from scraper import get_next_page_url

def test_get_next_page_url():
    ''' Test for get_next_page_url '''
    data = '<table align="center" height="15"><tr><td><b>Pages: </b><a href="?&amp;do_search=1&amp;searchword=computer&amp;order=popularad&amp;offset=0"><b><u>Prev</u></b></a> <b> <a href="?&amp;do_search=1&amp;searchword=computer&amp;order=popularad&amp;offset=0"><u>1</u></a> |</b><b><big> 2 </big>|</b><b> <a href="?&amp;do_search=1&amp;searchword=computer&amp;order=popularad&amp;offset=40"><u>3</u></a> |</b><b> <a href="?&amp;do_search=1&amp;searchword=computer&amp;order=popularad&amp;offset=60"><u>4</u></a> |</b><b> <a href="?&amp;do_search=1&amp;searchword=computer&amp;order=popularad&amp;offset=80"><u>5</u></a> |</b><b> <a href="?&amp;do_search=1&amp;searchword=computer&amp;order=popularad&amp;offset=100"><u>6</u></a> |</b><b> <a href="?&amp;do_search=1&amp;searchword=computer&amp;order=popularad&amp;offset=120"><u>7</u></a> |</b><b> <a href="?&amp;do_search=1&amp;searchword=computer&amp;order=popularad&amp;offset=140"><u>8</u></a> |</b><b> <a href="?&amp;do_search=1&amp;searchword=computer&amp;order=popularad&amp;offset=160"><u>9</u></a> |</b><b> <a href="?&amp;do_search=1&amp;searchword=computer&amp;order=popularad&amp;offset=180"><u>10</u></a> |</b><b> <a href="?&amp;do_search=1&amp;searchword=computer&amp;order=popularad&amp;offset=200"><u>11</u></a> |</b><b> <a href="?&amp;do_search=1&amp;searchword=computer&amp;order=popularad&amp;offset=380"><u>..20</u></a> </b><b> <a href="?&amp;do_search=1&amp;searchword=computer&amp;order=popularad&amp;offset=580"><u>...30</u></a> |</b> <a href="?&amp;do_search=1&amp;searchword=computer&amp;order=popularad&amp;offset=40"><b><u>Next</u></b></a> <br/><br/></td></tr></table>'

    expected_result = 'https://hamrobazaar.com/search.php?&do_search=1&searchword=computer&order=popularad&offset=40'
    actual_result = get_next_page_url(BeautifulSoup(data, 'html.parser'))

    assert actual_result == expected_result
