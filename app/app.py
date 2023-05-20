from hack import app, create_db, db
from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from hack.forms import LoginForm, RegForm, PredictForm
from hack.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from bs4 import BeautifulSoup
import requests
import pandas as pd
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
import dataGenerator as d
import leaderboardGenerator as l
import random

teamsDF = pd.read_csv('./data/Team.csv')

matchesTeamsDF = pd.read_csv("./data/gen/match_team.csv")
data = matchesTeamsDF.drop('Match_Id', axis=1)
data = data.drop('Unnamed: 0', axis=1)
X = data.drop('Match_Won', axis=1)
Y = data['Match_Won']
team_short_code = ''
opponent_short_code = ''

X = preprocessing.scale(X)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25)
        
create_db(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/leaderboard')
def leaderboard():
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    # s = requests.session()
    # url = s.get('https://www.hindustantimes.com/cricket/ipl/points-table', headers=headers).text
    # bs = BeautifulSoup(url, 'html.parser')
    # names = bs.find('table', class_='medalsTally').find_all('a', class_='hoverUnderline')
    # leaderboard = []
    # for i in names:
    #     name = i.find('span', class_='fullName whiteColorText').text
    #     leaderboard.append(name)
    leaderboard = l.team_data
    return render_template('leaderboard.html', leaderboard=leaderboard)

@app.route('/auth/new', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    mess=''
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            mess = 'An account with similar credentials already exists.'
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect('/')
    return render_template('reg.html', form=form, mess=mess)

@app.route('/auth/signin', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    mess=''
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            mess = 'Email not found.'
        else:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                mess = 'Incorrect password.'
    return render_template('login.html', mess=mess, form=form)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    global team_short_code, opponent_short_code
    form = PredictForm()
    mess = ''
    prediction = ''
    if form.validate_on_submit():
        if form.team1.data == form.team2.data:
            mess = 'Both teams cannot be the same.'
            prediction = ''
        teamCode = form.team1.data
        while len(teamsDF[teamsDF["Team_Short_Code"] == teamCode]) == 0:
            teamCode = form.team1.data
        team_short_code = teamCode

        opponentCode = form.team2.data
        while len(teamsDF[teamsDF["Team_Short_Code"] == opponentCode]) == 0:
            opponentCode = form.team2.data
        opponent_short_code = opponentCode
        teamId = teamsDF.loc[teamsDF["Team_Short_Code"] == teamCode, 'Team_Id'].values[0]
        opponentId = teamsDF.loc[teamsDF["Team_Short_Code"] == opponentCode, 'Team_Id'].values[0]

        tossCode = teamsDF.loc[teamsDF["Team_Short_Code"] == form.toss_winner.data, 'Team_Id'].values[0]
        while tossCode != teamId and tossCode != opponentId:
            tossCode = teamsDF.loc[teamsDF["Team_Short_Code"] == form.toss_winner.data, 'Team_Id'].values[0]

        tossWon = tossCode

        batCode = teamCode if tossWon == teamId else opponentCode

        while batCode != teamCode and batCode != opponentCode:
            batCode = teamCode if tossWon == teamId else opponentCode

        batFirst = teamsDF.loc[teamsDF["Team_Short_Code"] == batCode, 'Team_Id'].values[0]

        px = d.generatePredictData(int(teamId), int(opponentId), int(tossWon), int(batFirst))
        px = px.drop(['Match_Id', 'Match_Won'], axis=1)

        px = preprocessing.scale(px)

        lin_svm = svm.LinearSVC()
        lin_svm.fit(X_train, y_train)
        pred = lin_svm.predict(px)
        if pred[0] == 1:
            prediction = f'{team_short_code} has a greater chance of winning.'
        else:
            prediction = f'{opponent_short_code} has a greater chance of winning.'

    return render_template('predict.html', prediction=prediction, form=form, mess=mess)



@app.route('/auth/signout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
