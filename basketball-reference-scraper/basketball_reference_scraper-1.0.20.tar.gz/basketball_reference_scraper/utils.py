from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata

def get_game_suffix(date, team1, team2):
    r = get(f'https://www.basketball-reference.com/boxscores/index.fcgi?year={date.year}&month={date.month}&day={date.day}')
    suffix = None
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        for table in soup.find_all('table', attrs={'class': 'teams'}):
            for anchor in table.find_all('a'):
                if 'boxscores' in anchor.attrs['href']:
                    if team1 in anchor.attrs['href'] or team2 in anchor.attrs['href']:
                        suffix = anchor.attrs['href']
    return suffix

def get_player_suffix(name):
    normalized_name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8")
    names = normalized_name.split(' ')[1:]
    for last_name in names:
        initial = last_name[0].lower()
        r = get(f'https://www.basketball-reference.com/players/{initial}')
        if r.status_code==200:
            soup = BeautifulSoup(r.content, 'html.parser')
            for table in soup.find_all('table', attrs={'id': 'players'}):
                suffixes = []
                for anchor in table.find_all('a'):
                    if unicodedata.normalize('NFD', anchor.text).encode('ascii', 'ignore').decode("utf-8").lower() in name.lower():
                        suffix = anchor.attrs['href']
                        player_r = get(f'https://www.basketball-reference.com{suffix}')
                        if player_r.status_code==200:
                            player_soup = BeautifulSoup(player_r.content, 'html.parser')
                            h1 = player_soup.find('h1', attrs={'itemprop': 'name'})
                            if h1:
                                page_name = h1.find('span').text
                                if page_name.lower()==name.lower():
                                    return suffix


def remove_accents(name, team, season_end_year):
    alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXZY ')
    if len(set(name).difference(alphabet))==0:
        return name
    r = get(f'https://www.basketball-reference.com/teams/{team}/{season_end_year}.html')
    team_df = None
    best_match = name
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        team_df = pd.read_html(str(table))[0]
        max_matches = 0
        for p in team_df['Player']:
            matches = sum(l1 == l2 for l1, l2 in zip(p, name))
            if matches>max_matches:
                max_matches = matches
                best_match = p
    return best_match
