import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

###### Parameters

url_fifa_base = 'http://sofifa.com/players?'

fifa_stats = ['Crossing', 'Finishing', 'Heading Accuracy',
              'Short Passing', 'Volleys', 'Dribbling', 'Curve',
              'Free Kick Accuracy', 'Long Passing', 'Ball Control',
              'Acceleration', 'Sprint Speed', 'Agility', 'Reactions',
              'Balance', 'Shot Power', 'Jumping', 'Stamina', 'Strength',
              'Long Shots', 'Aggression', 'Interceptions', 'Positioning',
              'Vision', 'Penalties', 'Composure', 'Marking', 'Standing Tackle',
              'Sliding Tackle', 'GK Diving', 'GK Handling', 'GK Kicking',
              'GK Positioning', 'GK Reflexes']

countries = ['Russia', 'Brazil', 'Iran', 'Japan', 'Mexico', 'Belgium',
       'South Korea', 'Saudi Arabia', 'Germany', 'England', 'Spain',
       'Nigeria', 'Costa Rica', 'Poland', 'Egypt', 'Iceland', 'Serbia',
       'Portugal', 'France', 'Uruguay', 'Argentina', 'Colombia', 'Panama',
       'Senegal', 'Morocco', 'Tunisia', 'Switzerland', 'Croatia',
       'Sweden', 'Denmark', 'Australia', 'Peru', 'Korea Republic']

# nation IDs are between [1-251]
nations = 251

# the dates that we want to consider are 1 january of years 2018, 2014, 2010
days_code = [158961, 157501, 156090]
years_code = [18, 14, 10]

# number of top players to consider
n_players = 11


def soup_maker(url):
    r = requests.get(url)
    markup = r.content
    soup = bs(markup, 'lxml')
    return soup


def find_top_players(soup, n_players):
    table = soup.find('table', {'class': 'table-hover'})
    tbody = table.find('tbody')
    all_a = tbody.find_all('a', {'class': '', 'href': re.compile('player/')})
    final_results = []
    for player in all_a[:n_players]:
        final_details = {}
        final_details['short_name'] = player.text
        final_details.update(player_all_details('http://sofifa.com' + player['href']))
        print(final_details)
        final_results.append(final_details)
    return final_results


def find_player_info(soup):
    player_data = {}
    player_data['image'] = soup.find('img')['data-src']
    player_data['full_name'] = soup.find('h1').text.split(' (')[0]
    span = soup.find('span', attrs={'class': None}).contents[-1].strip()
    player_data['nation'] = soup.find('span', attrs={'class': None}).contents[1]['title']
    dob = re.search('\(.*\)', span).group(0)
    player_data['dob'] = dob.replace('(', '').replace(')', '')
    infos = span.replace(dob + ' ', '').split(' ')
    player_data['age'] = int(infos[infos.index('Age') + 1: -2][0])
    return (player_data)


def find_player_stats(soup):
    player_data = {}
    info = re.findall('\d+\.?\d?', soup.text)
    player_data['rating'] = float(info[0])
    player_data['potential'] = float(info[1])
    player_data['value'] = float(info[2])
    player_data['wage'] = float(info[3])
    return (player_data)


def player_all_details(url):
    all_details = {}
    print(url)
    soup = soup_maker(url)
    player_info = soup.find('div', {'class': 'player'})
    all_details.update(find_player_info(player_info))
    player_stats = soup.find('div', {'class': 'stats'})
    all_details.update(find_player_stats(player_stats))
    return all_details


def get_all_players_statistics_per_country_per_year(url_fifa_base, country, year, day, n_players):
    url = "{url_fifa_base}na%5B0%5D={country}&col=vl&sort=desc&v={year}&e={day}&set=true".format(
        url_fifa_base=url_fifa_base,
        country=country,
        year=year,
        day=day
    )
    print(url)

    soup = soup_maker(url)
    results_per_country_per_year = find_top_players(soup, n_players)
    results_per_country_per_year = pd.DataFrame(results_per_country_per_year)
    results_per_country_per_year['year'] = year
    results_per_country_per_year['country_code'] = country
    return results_per_country_per_year


def check_nation(url_fifa_base, country):
    url = "{url_fifa_base}na%5B0%5D={country}".format(
        url_fifa_base=url_fifa_base,
        country=country
    )
    soup = soup_maker(url)
    table = soup.find('table', {'class': 'table-hover'})
    tbody = table.find('tbody')
    all_a = tbody.find_all('a', {'class': ''})
    if len(all_a) == 0:
        return False
    return all_a[0]['title'] in countries


def query_all_fifa_players_info(nations, years_code, days_code, n_players):
    results_all = []
    for nation in range(1, nations):
        if check_nation(url_fifa_base, nation):
            for i in range(len(years_code)):
                try:
                    results = get_all_players_statistics_per_country_per_year(url_fifa_base, nation, years_code[i],
                                                                        days_code[i], n_players)
                    results_all.append(results)
                except:
                    print("it failed to get {} from year {} from nation {}.".format(i, years_code[i], nation))

            time.sleep(60)

    pd.concat(results_all).to_csv('./fifa_players_data.csv', index=False, encoding='utf-8')


query_all_fifa_players_info(nations, years_code, days_code, n_players)
