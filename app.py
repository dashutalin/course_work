from flask import Flask, render_template, request, g, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import psycopg2
from datetime import timedelta
from DataBase import DataBase
from UserLogin import UserLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wjjeojfej8y3uhjbf02qi8hh3962yvf'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
dbase = None


@login_manager.user_loader
def load_user(user_id):
    print(load_user)
    return UserLogin().fromDB(user_id, dbase)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='transportDB',
                            user='dashalin',
                            password='GP08139035')
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = get_db_connection()
    return g.link_db


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DataBase(db)


def check(res):
    if not res:
        return flash('Error', category='error')
    else:
        return flash('Good', category='success')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = dbase.getUserByEmail(request.form['login'])
        if user and user[2] == request.form['login']:
            user_login = UserLogin().create(user)
            login_user(user_login)
            if current_user.is_superuser():
                return redirect(url_for('showAdmin'))
            return redirect(url_for('newClaim'))
    return render_template('login.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        res = dbase.addUser(request.form['name'], request.form['login'], request.form['psw'])
        return redirect(url_for('login'))
    return render_template('reg.html')


@app.route('/claims')
@login_required
def showUser():
    claims = dbase.getUserClaims(current_user.get_id())
    return render_template('showUser.html', claims=claims)


@app.route('/new', methods=['GET', 'POST'])
@login_required
def newClaim():
    user_id = current_user.get_id()
    routes = dbase.getRoutes()
    if request.method == 'POST':
        route_id = dbase.getRouteId(request.form['route'])
        sum = dbase.getRoutePrice(route_id) * int(request.form['amount'])
        res = dbase.newUserClaim(int(route_id), int(user_id), request.form['date'], int(request.form['amount']), sum)
        # check(res)
        return redirect(url_for('showUser'))
    return render_template('newClaim.html', routes=list(routes))


@app.route('/show')
@login_required
def showAdmin():
    claims = dbase.getAdminClaims()
    return render_template('showAdmin.html', claims=claims)


@app.route('/show/<int:id_claim>', methods=['GET', 'POST'])
def showAdminClaim(id_claim):
    res = dbase.showAdminClaim(id_claim)
    drivers = dbase.showWorkers()
    buses = dbase.showBuses()
    if request.method == 'POST':
        if request.form['submit'] == 'Сохранить':
            bus = dbase.getBusId(request.form['buses'])
            driver = dbase.getWorkerId(request.form['drivers'])
            new = dbase.updateClaim(id_claim, str(driver), str(bus))
        else:
            new = dbase.deleteClaim(id_claim)
        return redirect(url_for('showAdmin'))
    return render_template('showAdminClaim.html', id=id_claim, res=res, drivers=list(drivers), buses=list(buses))


@app.route('/workers', methods=['GET', 'POST'])
@login_required
def addWorkers():
    if request.method == "POST":
        res = dbase.addWorker(request.form['name'], request.form['surname'], request.form['second_name'],
                              int(request.form['age']), request.form['passport'])
        # check(res)
    return render_template('workers.html')


@app.route('/allworkers')
@login_required
def showWorkers():
    workers = dbase.showWorkers()
    return render_template('allWorkers.html', workers=workers)


@app.route('/allworkers/<int:id_worker>', methods=['GET', 'POST'])
@login_required
def worker(id_worker):
    res = dbase.worker(id_worker)
    if request.method == 'POST':
        if request.form['submit'] == 'Сохранить':
            res = dbase.updateWorker(id_worker, request.form['name'], request.form['surname'], request.form['second_name'],
                              int(request.form['age']), request.form['passport'])
        else:
            res = dbase.deleteWorker(id_worker)
        return redirect(url_for('showWorkers'))
    return render_template('profileWorker.html', id=id_worker, res=res)


@app.route('/allbuses')
@login_required
def showBuses():
    buses = dbase.showBuses()
    return render_template('allBuses.html', buses=buses)


@app.route('/allbuses/<int:id_bus>', methods=['GET', 'POST'])
@login_required
def bus(id_bus):
    res = dbase.bus(id_bus)
    if request.method == 'POST':
        if request.form['submit'] == 'Сохранить':
            res = dbase.updateBus(id_bus, request.form['number'], request.form['model'], int(request.form['year']))
        else:
            res = dbase.deleteBus(id_bus)
        return redirect(url_for('showBuses'))
    return render_template('profileBus.html', id=id_bus, res=res)


@app.route('/buses', methods=['GET', 'POST'])
@login_required
def addBus():
    if request.method == 'POST':
        res = dbase.addBus(request.form['number'], request.form['model'], int(request.form['year']))
        # check(res)
    return render_template('buses.html')


@app.route('/routes', methods=['GET', 'POST'])
@login_required
def addRoute():
    if request.method == 'POST':
        res = dbase.addRoute(request.form['route'], int(request.form['days']), float(request.form['price']))
        # check(res)
    return render_template('routes.html')


@app.route('/allroutes')
@login_required
def showRoutes():
    routes = dbase.allRoutes()
    return render_template('allRoutes.html', routes=routes)


@app.route('/allroutes/<int:id_route>', methods=['GET', 'POST'])
@login_required
def route(id_route):
    res = dbase.route(id_route)
    if request.method == 'POST':
        if request.form['submit'] == 'Сохранить':
            res = dbase.updateRoute(id_route, request.form['route'], int(request.form['days']), float(request.form['price']))
        else:
            res = dbase.deleteRoute(id_route)
        return redirect(url_for('showRoutes'))
    return render_template('profileRoutes.html', id=id_route, res=res)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == '__main__':
    app.run()