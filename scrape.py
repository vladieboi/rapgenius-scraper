from framework import console, logger
from bs4 import BeautifulSoup
import requests
import json
import re
import os

def checkPath(path):
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

def scrape_track(url):
    song_url = url
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
        a = re.search(r'genius://songs/([0-9]*)', s.find('meta', attrs = {'property': 'twitter:app:url:iphone'}).get('content')).group(1)
        url = f'https://genius.com/api/songs/{a}'
        r = requests.get(url)
        if r.status_code == 200:
            j = json.loads(r.text)
            song_name = re.sub('\xa0', ' ', j['response']['song']['full_title'])
            artist_name = j['response']['song']['primary_artist']['name']
            artist_names = j['response']['song']['artist_names']
            artist_url = j['response']['song']['primary_artist']['url']
            album_name = j['response']['song']['album']['name']
            album_url = j['response']['song']['album']['url']
            release_date_song = j['response']['song']['release_date']
            release_date_album = f"{j['response']['song']['album']['release_date_components']['year']}-{str(j['response']['song']['album']['release_date_components']['month']).rjust(2, '0')}-{str(j['response']['song']['album']['release_date_components']['day']).rjust(2, '0')}"
            # console.print(f'{url} retrieved', color=console.OKGREEN)
            # logger.info(f'{url} retrieved')
            return {
                'song': song_name,
                'song_url': song_url,
                'artist': artist_name,
                'artists': artist_names,
                'artist_url': artist_url,
                'album': album_name,
                'album_url': album_url,
                'release_date_song': release_date_song,
                'release_date_album': release_date_album,
                'lyrics': t
            }
        else:
            console.print(f'{url} {r.status_code}', color=console.WARNING)
            logger.warning(f'{url} {r.status_code}')
            return None
    else:
        console.print(f'{url} {r.status_code}', color=console.WARNING)
        logger.warning(f'{url} {r.status_code}')
        return None
    
def scrape_album(url):
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
    r = requests.get(url)
    if r.status_code == 200:
        s = BeautifulSoup(r.text, 'html.parser')
        a = re.search(r'/artists/([0-9]*)', s.find('meta', attrs = {'name': 'newrelic-resource-path'}).get('content')).group(1)
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
    artist = 'https://genius.com/artists/Nane'
    albums = scrape_artist(artist)
    for album in albums:
        tracks = scrape_album(album)
        for track in tracks:
            scraped_track = scrape_track(track)
            if scraped_track != None:
                path = f'data'
                checkPath(path)
                path = f'data/{scraped_track["artist"]}'
                checkPath(path)
                path = f'data/{scraped_track["artist"]}/{scraped_track["album"]}'
                checkPath(path)
                path = f'data/{scraped_track["artist"]}/{scraped_track["album"]}/{scraped_track["song"]}.json'
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(scraped_track, f, ensure_ascii=False)

if __name__ == '__main__':
	main()