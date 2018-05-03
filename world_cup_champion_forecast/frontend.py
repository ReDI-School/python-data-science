import pickle

import pandas as pd
from flask import Flask, render_template
from flask import request

year = 2018
team_fer = pd.read_csv('team_features.csv')
logreg = pickle.load(open('Final_fifa_Logmodel.sav', 'rb'))

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
        'website.html', value1=value1, value2=value2,
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
    app.run(debug=True)
