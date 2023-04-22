from framework import console, logger
from bs4 import BeautifulSoup
import requests
import json
import re

def scrape_track(url):
    console.print(f'{url}')
    logger.info(f'{url}')
    r = requests.get(url)
    if r.status_code == 200:
        s = BeautifulSoup(r.text, 'html.parser')
        c = s.findAll('div', attrs = {'data-lyrics-container': 'true'})
        t = ''
        for _ in c:
            _ = re.sub('<br>', '\n', _.get_text(separator="\n"))
            t += _
        l = len(t.split("\n"))
        console.print(f'{url} ({l} lyrics)', color=console.OKGREEN)
        logger.info(f'{url} ({l} lyrics)')
        return t
    else:
        console.print(f'{url} {r.status_code}', color=console.WARNING)
        logger.warning(f'{url} {r.status_code}')
        return None
    
def scrape_album(url):
    console.print(f'{url}')
    logger.info(f'{url}')
    r = requests.get(url)
    if r.status_code == 200:
        s = BeautifulSoup(r.text, 'html.parser')
        c = s.find('div', class_ = 'column_layout u-top_margin').findAll('a', class_ = 'u-display_block')
        l = []
        for _ in c:
            l.append(_.get('href'))
        console.print(f'{url} ({len(l)} tracks)', color=console.OKGREEN)
        logger.info(f'{url} ({len(l)} tracks)')
        return l
    else:
        console.print(f'{url} {r.status_code}', color=console.WARNING)
        logger.warning(f'{url} {r.status_code}')
        return None

def scrape_artist(url):
    console.print(f'{url}')
    logger.info(f'{url}')
    r = requests.get(url)
    if r.status_code == 200:
        s = BeautifulSoup(r.text, 'html.parser')
        a = re.search(r'/artists/([0-9]*)', s.find('meta', attrs = {'name': 'newrelic-resource-path'}).get('content')).group(1)
        # while True:
        l = []
        p = 1
        page_loop = True
        while page_loop == True:
            url = f'https://genius.com/api/artists/{a}/albums?page={p}'
            r = requests.get(url)
            if r.status_code == 200:
                j = json.loads(r.text)
                for album in j['response']['albums']:
                    l.append(album['url'])
                if j['response']['next_page'] != None:
                    p = j['response']['next_page']
                else:
                    page_loop = False
                    url = re.sub(r'\?page=.*', '', url)
                    console.print(f'{url} ({len(l)} albums)', color=console.OKGREEN)
                    logger.info(f'{url} ({len(l)} albums)')
                    return l
            else:
                console.print(f'{url} {r.status_code}', color=console.WARNING)
                logger.warning(f'{url} {r.status_code}')
                return None        
    else:
        console.print(f'{url} {r.status_code}', color=console.WARNING)
        logger.warning(f'{url} {r.status_code}')
        return None

def main():
    albums = scrape_artist('https://genius.com/artists/Nane')
    for album in albums:
        tracks = scrape_album(album)
        for track in tracks:
            track_lyrics = scrape_track(track)

if __name__ == '__main__':
	main()