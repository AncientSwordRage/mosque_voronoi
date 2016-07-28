"""Scrape command."""
from django.core.management.base import BaseCommand # NOQA
#from mosque_scraper.models import Mosque  # NOQA
import datetime
import string
import requests
import re
from bs4 import BeautifulSoup as bs4  # NOQA

directory_url = 'http://www.mosquedirectory.co.uk/browse-mosques/alphabet/letter/{letter}/{page}/'


class Command(BaseCommand):
    """Scape the site for mosques."""

    help = 'Scrapes the sites for mosques'

    def handle(self, *args, **options):
        """Handle McHandleface."""
        self.stdout.write('\nScapping mosques, started at {time}'.format(time=datetime.datetime.now()))
        # go though all the letters
        for letter in string.ascii_uppercase:
            url = directory_url.format(page='1', letter=letter)
            # get the page for that letter
            root = self.get_mosque_list(url)
            # get all the pages, except the first one (not an 'a' element)
            page_list = [a.text for a in root.select('#search_data_results > a')
                         if a.text.isdigit()]
            for page in page_list:
                # get mosques from last page
                mosques = root.select('#mosque_list li')
                for mosque in mosques:
                    self.extract_mosque(mosque, page)
                url = directory_url.format(page=page, letter=letter)
                # update root from within loop
                root = self.get_mosque_list(url)

    def get_mosque_list(self, url):
        """Get list of mosques on page."""
        r = requests.get(url)
        root = bs4(r.content, 'html.parser')
        return root

    def extract_mosque(self, mosque, page):
        """Extract Mosque."""
        mosque_text = re.sub(u"(\u2018|\u2019)", "'", mosque.text)
        mosque_link = mosque.get('href')
        self.stdout.write('\nWriting {} to file, from page {}'.format(mosque_text, page))
        mosque_page = bs4(requests.get(mosque_link).content)
        mosque_info_rows = mosque_page.select('#mosque_info_contents table table tr')
        values = {cells[0].replace(':').lowercase(): cells[1]
                  for row in mosque_info_rows
                  for cells in row.find_all('td')}
        name_address = mosque_page.select('#results h1:first-of-type')
        matches = re.match(r'(?P<name>[^(]*)\((?P<address>[^)]*)\))', name_address)
        values['name'] = matches.group('name')
        values['rating'] = mosque_page.select('.star_rating strong')