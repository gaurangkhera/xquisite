from hack import app, create_db, db
from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from hack.forms import LoginForm, RegForm, PredictForm
from hack.models import User, Stadium, Seat
from werkzeug.security import generate_password_hash, check_password_hash
from bs4 import BeautifulSoup
import requests
import pandas as pd
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
import dataGenerator as d
import leaderboardGenerator as l
import random
import stripe

stripe.api_key = app.config['STRIPE_SECRET_KEY']
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
#     stadium = Stadium(name='M.A. Chidambaram Stadium', match='GT vs CSK')
#     db.session.add(stadium)
#     db.session.commit()
#     for i in range(25):
#         seat = Seat(price=2500, category='Fourth class', stadium=1)
#         db.session.add(seat)
#         db.session.commit()
#     for i in range(25):
#         seat = Seat(price=4000, category='Third class', stadium=1)
#         db.session.add(seat)
#         db.session.commit()
#     for i in range(25):
#         seat = Seat(price=6000, category='Second class', stadium=1)
#         db.session.add(seat)
#         db.session.commit()
#     for i in range(25):
#         seat = Seat(price=10000, category='First class', stadium=1)
#         db.session.add(seat)
#         db.session.commit()
    return render_template('index.html')

@app.route('/upgraded/<membership>', methods=['GET', 'POST'])
@login_required
def upgraded(membership):
    current_user.membership = membership.title()
    if membership == "Premium":
        current_user.predictions = 20
    if membership == "Pro":
        current_user.predictions = 50
    if membership == "Elite":
        current_user.predictions = 100
    db.session.add(current_user)
    db.session.commit()
    return render_template('thankyouupgrade.html')

@app.route('/upgrade')
@login_required
def upgrade():
    return render_template('membership.html', key=app.config['STRIPE_PUBLISHABLE_KEY'])

@app.route('/deleteseat/<id>')
def delete_seat(id):
    seat = Seat.query.filter_by(id=id).first()
    current_user.seats_bought.remove(seat)
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('cart'))

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

@app.route('/bookseats')
@login_required
def book_seat():
    seats = Seat.query.all()
    stadiums = Stadium.query.filter_by(id=1).first()
    total = 0
    for i in current_user.seats_bought:
        total += i.price
    return render_template('bookseat.html', seats=seats, stadium=stadiums, total=total, key=app.config['STRIPE_PUBLISHABLE_KEY'])

@app.route('/cart')
def cart():
    total = 0
    subtotal = 0
    interest = 0
    for s in current_user.seats_bought:
        subtotal += s.price
    if subtotal > 5000:
        interest = 5/100
        total = subtotal + subtotal * interest
    else:
        interest = 15/100
        total = subtotal + subtotal * interest
    premium = total - 5/100 * total
    pro = total - 10/100 * total
    elite = total - 14/100 * total
    return render_template('cart.html', total=total, key=app.config['STRIPE_PUBLISHABLE_KEY'], tax=interest, subtotal=subtotal, premium=premium, pro=pro, elite=elite)

@app.route('/buyseats')
@login_required
def buy_cart():
        total = 0
        for i in current_user.seats_bought:
            total += i.price
        customer = stripe.Customer.create(
                email=current_user.email,
                source=request.form['stripeToken']
            )

        stripe.Charge.create(
                customer=customer.id,
                amount=total,
                currency='inr',
                description='Seat purchase'
            )
        return redirect(url_for('thank_you'))  
    
@app.route('/thankyou', methods=['GET', 'POST'])
@login_required
def thank_you():
    for i in current_user.seats_bought:
        i.taken = 1
        db.session.add(i)
        db.session.commit()
    current_user.seats_bought = []
    db.session.add(current_user)
    db.session.commit()
    return render_template('thankyou.html')

@app.route('/select_seat/<id>')
@login_required
def select_seat(id):
    seat = Seat.query.filter_by(id=id).first()
    current_user.seats_bought.append(seat)
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('book_seat'))

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
@login_required
def predict():
    if current_user.used < current_user.predictions:
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

    else:
        return redirect(url_for('upgrade'))
    current_user.used += 1
    db.session.add(current_user)
    db.session.commit()
    return render_template('predict.html', prediction=prediction, form=form, mess=mess)



@app.route('/auth/signout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
