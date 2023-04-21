from framework import console, logger
from bs4 import BeautifulSoup
import requests
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
        console.print(f'{url} ({l} lines)', color=console.OKGREEN)
        logger.info(f'{url} ({l} lines)')
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

def main():
    tracks = scrape_album('https://genius.com/albums/Nane/Avram')
    for track in tracks:
        track_lyrics = scrape_track(track)

if __name__ == '__main__':
	main()