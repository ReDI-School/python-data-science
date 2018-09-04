import pickle

import pandas as pd
from flask import Flask, render_template
from flask import request

year = 2018
team_fer = pd.read_csv('team_features.csv')
logreg = pickle.load(open('Final_fifa_Logmodel.sav', 'rb'))

countries = ['Argentina', 
             'Australia', 
             'Belgium', 
             'Brazil', 
             'Colombia', 
             'Costa Rica', 
             'Croatia',
             'Denmark', 
             'Egypt', 
             'England', 
             'France', 
             'Germany', 
             'Iceland', 
             'Iran', 
             'Japan', 
             'Korea',
             'Mexico', 
             'Morocco', 
             'Nigeria', 
             'Panama', 
             'Paraguay', 
             'Peru', 
             'Poland', 
             'Russia', 
             'Saudi Arabia',
             'Senegal', 
             'Serbia', 
             'Spain',
             'Sweden', 
             'Switzerland', 
             'Tunisia', 
             'Uruguay']

country_codes = dict({'Algeria':    'dz', 
                      'Argentina':  'ar', 
                      'Australia':  'au', 
                      'Belgium':    'be', 
                      'Brazil':     'br', 
                      'Cameroon':   'cm', 
                      'Chile':      'cl', 
                      'Colombia':   'co', 
                      'Costa Rica': 'cr', 
                      'Croatia':    'hr', 
                      'Denmark':    'dk', 
                      'Ecuador':    'ec', 
                      'Egypt':      'eg', 
                      'England':    'gb', 
                      'France':     'fr', 
                      'Germany':    'de', 
                      'Ghana':      'gh', 
                      'Greece':     'gr', 
                      'Honduras':   'hn', 
                      'Iceland':    'is', 
                      'Iran':       'ir', 
                      'Italy':      'it', 
                      'Ivory Coast':'ci', 
                      'Japan':      'jp', 
                      'Mexico':     'mx', 
                      'Morocco':    'ma', 
                      'Netherlands':'nl', 
                      'New Zealand':'nz', 
                      'Nigeria':    'ng', 
                      'Panama':     'pa', 
                      'Paraguay':   'py', 
                      'Peru':       'pe', 
                      'Poland':     'pl', 
                      'Portugal':   'pt', 
                      'Russia':     'ru', 
                      'Saudi Arabia':'sa', 
                      'Senegal':    'sn', 
                      'Serbia':     'rs', 
                      'Slovakia':   'sk', 
                      'Slovenia':   'si', 
                      'South Africa':'za', 
                      'Korea': 'kr', 
                      'Spain':      'es', 
                      'Sweden':     'se', 
                      'Switzerland':'ch', 
                      'Tunisia':    'tn', 
                      'United States':'us', 
                      'Uruguay':    'uy'})

app = Flask(__name__)


@app.route('/static')
def root():
    return app.send_static_file('index.html')


@app.route("/")
def template_test():
    value1 = request.args.get('country', default="", type=str)
    value2 = request.args.get('country2', default="", type=str)
    if (value1 == "") or (value2 == ''):
        result = None
    else:
        result = predict(value1, value2, year, team_fer, logreg)

    return render_template(
        'website.html', countries=countries, country_codes=country_codes, country1=value1, country2=value2,
        result=result)


def getval(team1, team2, year, df):
    team1_par = df[(df["nation"] == team1) & (df["year"] == year)].iloc[0]
    team2_par = df[(df["nation"] == team2) & (df["year"] == year)].iloc[0]
    rank_dif = team1_par["Fifa Ranking"] - team2_par["Fifa Ranking"]
    rate_dif = team1_par["rating"] - team2_par["rating"]
    return rank_dif, rate_dif


def predict(team1, team2, year, df, logreg):
    ex1 = getval(team1, team2, year, df)
    log = logreg.predict([list(ex1)])[0]
    if log == 1:
        return team2
    else:
        return team1


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
