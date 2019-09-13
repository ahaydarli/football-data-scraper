from app import app
from flask import render_template, flash, redirect, jsonify, session
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, current_user, login_required, logout_user
from app.models import User, Country, Leagues, Club, Year, Week, WeekClubs
from flask import url_for, request
from werkzeug.urls import url_parse
from app import db
from app.methods import Crawler
import time
import requests
from bs4 import BeautifulSoup
import re

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/change_theme/<string:theme>')
def change_theme(theme):
    session['theme'] = theme
    return redirect(request.referrer)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid pass or username')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/countries')
def countries():
    countries = Country.query.all()
    return render_template('countries.html', countries=countries)


@app.route('/league/<int:country_id>')
def leagues(country_id):
    leagues = Leagues.query.filter_by(country_id=country_id)
    return render_template('leagues.html', leagues=leagues)


@app.route('/club/<int:year_id>')
def clubs(year_id):
    club = Club.query.filter_by(year_id=year_id)
    return render_template('clubs.html', clubs=club, week=week)


@app.route('/year/<int:league_id>')
def years(league_id):
    year = Year.query.filter_by(league_id=league_id).all()
    return render_template('year.html', year=year)


@app.route('/week/<int:year_id>')
def week(year_id):
    week = Week.query.filter_by(year_id=year_id)
    return render_template('week.html', week=week)


@app.route('/week-clubs/<int:week_id>')
def week_clubs(week_id):
    week = Week.query.filter_by(id=week_id).one()
    clubs = WeekClubs.query.filter_by(week_id=week_id)
    return render_template('clubs.html', clubs=clubs, week=week)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/team-table')
def team_table():
    return render_template('team-table.html')


@app.route('/scrap', methods=['GET', 'POST'])
def scrap():
    home_team = request.args.get('home_team')
    away_team = request.args.get('away_team')
    if home_team and away_team:
        data = Crawler.trade_spider(home_team, away_team)
        return render_template('team_scores.html', data=data)
    return render_template('team_form.html')


#get countries and save to db
@app.route('/scrap_countries')
def scrap_countries():
    data = Crawler.get_countries('http://wildstat.com/p/20')
    for item in data:
        country = Country.query.filter_by(country_id=data[item]).first()
        if country is None:
            country = Country(country_id=data[item], name=item)
            db.session.add(country)
            db.session.commit()
    return 'ok'


#get leagues by country
@app.route('/scrap_league')
def scrap_leagues():
    leagues = {}
    countries = Country.query.all()
    for item in countries:
        url = 'http://wildstat.com/p/{}'.format(item.country_id)
        leagues[item.country_id] = Crawler.get_leagues(url)
        time.sleep(0.3)
    for item in leagues:
        for league in leagues[item]:
            leag = Leagues(country_id=item, name=league, league_id=leagues[item][league])
            db.session.add(leag)
            db.session.commit()
    return jsonify(leagues)


@app.route('/scrap_years')
def scrap_years():
    years = {}
    leagues = Leagues.query.all()
    for item in leagues:
        url = 'http://wildstat.com/p/{}'.format(item.league_id)
        years[item.league_id] = Crawler.get_years(url)
        time.sleep(0.2)
    for item in years:
        for year in years[item]:
            y = Year(league_id=item, name=year, url=years[item][year])
            db.session.add(y)
            db.session.commit()
            print(y)
    return jsonify(years)


@app.route('/scrap_clubs')
def scrap_clubs():
    clubs = {}
    year = Year.query.filter_by(league_id=2301).limit(10)
    for item in year:
        url = 'http://wildstat.com/{}'.format(item.url)
        clubs[item.id] = Crawler.get_club(url)
        time.sleep(0.2)
    for item in clubs:
        for club in clubs[item]:
            c = Club(year_id=item, name=club, url=clubs[item][club])
            db.session.add(c)
            db.session.commit()
    return jsonify(clubs)


@app.route('/scrap_weeks')
def scrap_weeks():
    weeks = {}
    year = Year.query.filter_by(league_id=2301).limit(20)
    for item in year:
        url = 'http://wildstat.com/{}'.format(item.url)
        weeks[item.id] = Crawler.get_week(url)
        time.sleep(5)
    for item in weeks:
        for week in weeks[item]:
            w = Week(year_id=item, name=week, url=weeks[item][week])
            db.session.add(w)
            db.session.commit()
    return jsonify(weeks)


@app.route('/scrap_week_clubs')
def scrap_week_clubs():
    clubs = {}
    week = Week.query.filter_by(year_id=1312).limit(20)
    for item in week:
        url = 'http://wildstat.com/{}'.format(item.url)
        clubs[item.id] = Crawler.get_table(url)
        time.sleep(5)
        for club in clubs[item.id]:
            c = WeekClubs(
                          week_id=item.id, name=club[0], url='',
                          game=club[1], win=club[2], draw=club[3],
                          lost=club[4], f=Crawler.f(club[5]), a=Crawler.a(club[5]),
                          pound=club[6], home_win=club[7], home_draw=club[8],
                          home_lost=club[9], home_f=Crawler.f(club[10]), home_a=Crawler.a(club[10]),
                          home_pound=club[11], away_win=club[12], away_draw=club[13],
                          away_lost=club[14], away_f=Crawler.f(club[15]), away_a=Crawler.a(club[15]),
                          away_pound=club[16]
                          )
            db.session.add(c)
            db.session.commit()
    return jsonify(clubs)

@app.route('/get_table')
def get_table():
    clubs = []
    url = 'http://wildstat.com/p/2301/ch/ENG_1_2004_2005/stg/all/tour/all'
    source = requests.get(url)
    plain_text = source.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    for item in soup.find_all('table', {'class': 'championship'}):
        for tr in item.find_all('tr'):
            data = []
            for td in tr.find_all('td'):
                if td.text:
                    data.append(td.text)
                # if str.isdigit(td.text) and re.match("^[0-9.]*$", td.text):
                #     data.append(td.text)
                # for a in td.find_all('a', href=True):
                    # if str.isdigit(a.text) and re.match("^[0-9.]*$", a.text):
                    #     data.append(a.text)
            if data:
                data.pop(0)
                if len(data) == 18:
                    data.pop(7)
                clubs.append(data)
        break
    # return jsonify(Crawler.f(clubs[5]))
    return jsonify(clubs[2:])






