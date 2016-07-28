"""Scrape command."""
from django.core.management.base import BaseCommand # NOQA
from mosque_scraper.models import Mosque  # NOQA
import datetime
import string
import requests
import re
from bs4 import BeautifulSoup as bs4  # NOQA

root_url = 'http://www.mosquedirectory.co.uk'
directory_url = root_url + '/browse-mosques/alphabet/letter/{letter}/{page}/'


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
        fields = [field.attname.replace('_id', '')
                  for field in Mosque._meta.fields
                  if field.attname != 'id']
        mosque_text = re.sub(u"(\u2018|\u2019)", "'", mosque.text)
        mosque_link = '/'.join([root_url, mosque.find('a').get('href').split('../')[-1]])
        log_text = '\nWriting {} to file, from page {}'
        self.stdout.write(log_text.format(mosque_text, page))
        mosque_page = bs4(requests.get(mosque_link).content, 'html.parser')
        rows_selector = '#mosque_info_contents table table tr'
        mosque_info_rows = mosque_page.select(rows_selector)
        values = {}
        # page is a giant table, so go over the rows
        for row in mosque_info_rows:
            cells = row.find_all('td')
            # check we have the right fields
            try:
                key = cells[0].text.replace(':', '').lower().strip().replace(' ', '_')
            except (IndexError, AttributeError):
                import pdb; pdb.set_trace()
                # if no key or replace atribute, probably don't want it
                continue
            if len(cells) == 2 and key in fields:
                values[key] = cells[1].text
        name_address = mosque_page.select('#results h1')
        matches = re.match(r'(?P<name>[^(]*)\(', name_address[0].text)
        values['name'] = matches.group('name').strip()
        values['rating'] = mosque_page.select('.star_rating strong')[0].text
        values['mdpk'] = mosque_link.split('/')[-1]
        self.stdout.write(str(set(values.keys()) ^ set(fields)))
