from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)
act_name = 0
act_pass = 0


@app.route('/update')  # обновление данных каталога
def update():
    db_file = 'db/sites_base.sqlite'
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    titles = cur.execute(f"SELECT name FROM sites").fetchall()
    for i in titles:
        from parsing_sites import connection
        des = connection.pars(i[0])
        data = (des, i[0])
        cur.execute("UPDATE sites SET descrip = ? WHERE name = ?", data)
    con.commit()
    rows = len(cur.execute("SELECT * FROM sites").fetchall())
    titles = cur.execute("SELECT name FROM sites").fetchall()
    type__ = cur.execute("SELECT type FROM sites").fetchall()
    age = cur.execute("SELECT age FROM sites").fetchall()
    type_age = [type__[i][0] + ', ' + age[i][0] for i in range(len(type__))]
    links = cur.execute("SELECT link FROM sites").fetchall()
    img = cur.execute("SELECT img FROM sites").fetchall()
    description = cur.execute("SELECT descrip FROM sites").fetchall()
    if act_name == 0:
        return render_template('catalog.html', n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)
    else:
        return render_template('catalog_acc.html', form_name=act_name, n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)


@app.route('/')  # главная страница без аккаунта
def index():
    global act_name
    if act_name == 0:
        return render_template('homepage.html')
    else:
        return render_template('hpage_acc.html', form_name=act_name)


@app.route('/search', methods=['GET', 'POST'])  # поиск и переход в каталог
def search():
    global act_name, act_pass
    sc = request.form['sear']
    db_file = 'db/users_base.sqlite'
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    if act_name != 0 and act_pass != 0:
        old_his = cur.execute(f"SELECT history FROM users WHERE name = '{act_name}' AND password = '{act_pass}'").fetchall()
        if str(old_his[0][0]) != 'None':
            new_his = str(old_his[0][0]) + ', ' + sc
        else:
            new_his = sc
        data = (new_his, act_name, act_pass)
        cur.execute("UPDATE users SET history = ? WHERE name = ? AND password = ?", data)
        con.commit()
    cur.close()
    db_file = 'db/sites_base.sqlite'
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    res_name = cur.execute(f'SELECT * FROM sites WHERE name LIKE "%{sc}%"').fetchall()
    res_type = cur.execute(f'SELECT * FROM sites WHERE type LIKE "%{sc}%"').fetchall()
    if res_type:
        rows = len(cur.execute(f"SELECT * FROM sites WHERE type LIKE '%{sc}%'").fetchall())
        titles = cur.execute(f"SELECT name FROM sites WHERE type LIKE '%{sc}%'").fetchall()
        type__ = cur.execute(f"SELECT type FROM sites WHERE type LIKE '%{sc}%'").fetchall()
        age = cur.execute(f"SELECT age FROM sites WHERE type LIKE '%{sc}%'").fetchall()
        type_age = [type__[i][0] + ', ' + age[i][0] for i in range(len(type__))]
        links = cur.execute(f"SELECT link FROM sites WHERE type LIKE '%{sc}%'").fetchall()
        img = cur.execute(f"SELECT img FROM sites WHERE type LIKE '%{sc}%'").fetchall()
        description = cur.execute(f"SELECT descrip FROM sites WHERE type LIKE '%{sc}%'").fetchall()
        if act_name == 0:
            return render_template('catalog.html', n=rows, game_names=titles, game_types=type_age,
                                   game_descriptions=description, game_links=links, game_img=img)
        else:
            return render_template('catalog_acc.html', form_name=act_name, n=rows, game_names=titles,
                                   game_types=type_age,
                                   game_descriptions=description, game_links=links, game_img=img)
    if res_name:
        rows = len(cur.execute(f'SELECT * FROM sites WHERE name LIKE "%{sc}%"').fetchall())
        titles = cur.execute(f'SELECT name FROM sites WHERE name LIKE "%{sc}%"').fetchall()
        type__ = cur.execute(f"SELECT type FROM sites WHERE name LIKE '%{sc}%'").fetchall()
        age = cur.execute(f"SELECT age FROM sites WHERE name LIKE '%{sc}%'").fetchall()
        type_age = [type__[i][0] + ', ' + age[i][0] for i in range(len(type__))]
        links = cur.execute(f"SELECT link FROM sites WHERE name LIKE '%{sc}%'").fetchall()
        img = cur.execute(f"SELECT img FROM sites WHERE name LIKE '%{sc}%'").fetchall()
        description = cur.execute(f"SELECT descrip FROM sites WHERE name LIKE '%{sc}%'").fetchall()
        if act_name == 0:
            return render_template('catalog.html', n=rows, game_names=titles, game_types=type_age,
                                   game_descriptions=description, game_links=links, game_img=img)
        else:
            return render_template('catalog_acc.html', form_name=act_name, n=rows, game_names=titles,
                                   game_types=type_age,
                                   game_descriptions=description, game_links=links, game_img=img)
    if res_name is not True and res_type is not True:
        if act_name == 0:
            return render_template('fail_search.html')
        else:
            return render_template('fail_acc.html', form_name=act_name)


@app.route('/login')  # страница авторизации
def login():
    return render_template('loginpage.html', fail_log='')


@app.route('/account')  # страница выхода из аккаунта
def account():
    global act_name, act_pass
    db_file = 'db/users_base.sqlite'
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    res = cur.execute(f"SELECT history FROM users WHERE name = '{act_name}' AND password = '{act_pass}'").fetchall()
    if str(res[0][0]) != 'None':
        return render_template('accountswitch.html', form_name=act_name, his=res[0][0])
    return render_template('accountswitch.html', form_name=act_name, his='История отсутствует')


@app.route('/signin')  # страница регистрации
def sign():
    return render_template('signinpage.html', fail_sign='')


@app.route('/katalog')  # страница каталога
def cat():
    db_file = 'db/sites_base.sqlite'
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    rows = len(cur.execute("SELECT * FROM sites").fetchall())
    titles = cur.execute("SELECT name FROM sites").fetchall()
    type__ = cur.execute("SELECT type FROM sites").fetchall()
    age = cur.execute("SELECT age FROM sites").fetchall()
    type_age = [type__[i][0] + ', ' + age[i][0] for i in range(len(type__))]
    links = cur.execute("SELECT link FROM sites").fetchall()
    img = cur.execute("SELECT img FROM sites").fetchall()
    description = cur.execute("SELECT descrip FROM sites").fetchall()
    if act_name == 0:
        return render_template('catalog.html', n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)
    else:
        return render_template('catalog_acc.html', form_name=act_name, n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)


@app.route('/video')  # каталог-видео
def video():
    db_file = 'db/sites_base.sqlite'
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    rows = len(cur.execute("SELECT * FROM sites WHERE type in ('Видео-уроки')").fetchall())
    titles = cur.execute("SELECT name FROM sites WHERE type in ('Видео-уроки')").fetchall()
    type__ = cur.execute("SELECT type FROM sites WHERE type in ('Видео-уроки')").fetchall()
    age = cur.execute("SELECT age FROM sites WHERE type in ('Видео-уроки')").fetchall()
    type_age = [type__[i][0] + ', ' + age[i][0] for i in range(len(type__))]
    links = cur.execute("SELECT link FROM sites WHERE type in ('Видео-уроки')").fetchall()
    img = cur.execute("SELECT img FROM sites WHERE type in ('Видео-уроки')").fetchall()
    description = cur.execute("SELECT descrip FROM sites WHERE type in ('Видео-уроки')").fetchall()
    if act_name == 0:
        return render_template('catalog.html', n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)
    else:
        return render_template('catalog_acc.html', form_name=act_name, n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)


@app.route('/games')  # каталог-игры
def games():
    db_file = 'db/sites_base.sqlite'
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    rows = len(cur.execute("SELECT * FROM sites WHERE type in ('Игры')").fetchall())
    titles = cur.execute("SELECT name FROM sites WHERE type in ('Игры')").fetchall()
    type__ = cur.execute("SELECT type FROM sites WHERE type in ('Игры')").fetchall()
    age = cur.execute("SELECT age FROM sites WHERE type in ('Игры')").fetchall()
    type_age = [type__[i][0] + ', ' + age[i][0] for i in range(len(type__))]
    links = cur.execute("SELECT link FROM sites WHERE type in ('Игры')").fetchall()
    img = cur.execute("SELECT img FROM sites WHERE type in ('Игры')").fetchall()  # width="237" height="151"
    description = cur.execute("SELECT descrip FROM sites WHERE type in ('Игры')").fetchall()
    if act_name == 0:
        return render_template('catalog.html', n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)
    else:
        return render_template('catalog_acc.html', form_name=act_name, n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)


@app.route('/less')  # каталог-занятия
def less():
    db_file = 'db/sites_base.sqlite'
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    rows = len(cur.execute("SELECT * FROM sites WHERE type in ('Развлекательные занятия')").fetchall())
    titles = cur.execute("SELECT name FROM sites WHERE type in ('Развлекательные занятия')").fetchall()
    type__ = cur.execute("SELECT type FROM sites WHERE type in ('Развлекательные занятия')").fetchall()
    age = cur.execute("SELECT age FROM sites WHERE type in ('Развлекательные занятия')").fetchall()
    type_age = [type__[i][0] + ', ' + age[i][0] for i in range(len(type__))]
    links = cur.execute("SELECT link FROM sites WHERE type in ('Развлекательные занятия')").fetchall()
    img = cur.execute("SELECT img FROM sites WHERE type in ('Развлекательные занятия')").fetchall()
    description = cur.execute("SELECT descrip FROM sites WHERE type in ('Развлекательные занятия')").fetchall()
    if act_name == 0:
        return render_template('catalog.html', n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)
    else:
        return render_template('catalog_acc.html', form_name=act_name, n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)


@app.route('/two-three')  # каталог-2-3
def two_three():
    db_file = 'db/sites_base.sqlite'
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    rows = len(cur.execute("SELECT * FROM sites WHERE age in ('от 2-3 лет')").fetchall())
    titles = cur.execute("SELECT name FROM sites WHERE age in ('от 2-3 лет')").fetchall()
    type__ = cur.execute("SELECT type FROM sites WHERE age in ('от 2-3 лет')").fetchall()
    age = cur.execute("SELECT age FROM sites WHERE age in ('от 2-3 лет')").fetchall()
    type_age = [type__[i][0] + ', ' + age[i][0] for i in range(len(type__))]
    links = cur.execute("SELECT link FROM sites WHERE age in ('от 2-3 лет')").fetchall()
    img = cur.execute("SELECT img FROM sites WHERE age in ('от 2-3 лет')").fetchall()
    description = cur.execute("SELECT descrip FROM sites WHERE age in ('от 2-3 лет')").fetchall()
    if act_name == 0:
        return render_template('catalog.html', n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)
    else:
        return render_template('catalog_acc.html', form_name=act_name, n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)


@app.route('/three-four')  # каталог-3-4
def three_four():
    db_file = 'db/sites_base.sqlite'
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    rows = len(cur.execute("SELECT * FROM sites WHERE age in ('от 3-4 лет')").fetchall())
    titles = cur.execute("SELECT name FROM sites WHERE age in ('от 3-4 лет')").fetchall()
    type__ = cur.execute("SELECT type FROM sites WHERE age in ('от 3-4 лет')").fetchall()
    age = cur.execute("SELECT age FROM sites WHERE age in ('от 3-4 лет')").fetchall()
    type_age = [type__[i][0] + ', ' + age[i][0] for i in range(len(type__))]
    links = cur.execute("SELECT link FROM sites WHERE age in ('от 3-4 лет')").fetchall()
    img = cur.execute("SELECT img FROM sites WHERE age in ('от 3-4 лет')").fetchall()
    description = cur.execute("SELECT descrip FROM sites WHERE age in ('от 3-4 лет')").fetchall()
    if act_name == 0:
        return render_template('catalog.html', n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)
    else:
        return render_template('catalog_acc.html', form_name=act_name, n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)


@app.route('/four-five')  # каталог-4-5
def four_five():
    db_file = 'db/sites_base.sqlite'
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    rows = len(cur.execute("SELECT * FROM sites WHERE age in ('от 4-5 лет')").fetchall())
    titles = cur.execute("SELECT name FROM sites WHERE age in ('от 4-5 лет')").fetchall()
    type__ = cur.execute("SELECT type FROM sites WHERE age in ('от 4-5 лет')").fetchall()
    age = cur.execute("SELECT age FROM sites WHERE age in ('от 4-5 лет')").fetchall()
    type_age = [type__[i][0] + ', ' + age[i][0] for i in range(len(type__))]
    links = cur.execute("SELECT link FROM sites WHERE age in ('от 4-5 лет')").fetchall()
    img = cur.execute("SELECT img FROM sites WHERE age in ('от 4-5 лет')").fetchall()
    description = cur.execute("SELECT descrip FROM sites WHERE age in ('от 4-5 лет')").fetchall()
    if act_name == 0:
        return render_template('catalog.html', n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)
    else:
        return render_template('catalog_acc.html', form_name=act_name, n=rows, game_names=titles, game_types=type_age,
                               game_descriptions=description, game_links=links, game_img=img)


@app.route('/get-text', methods=['GET', 'POST'])  # регистрация, получение логина и пароля
def foo():
    global act_name, act_pass
    check = ''
    bar = request.form['login']
    bur = request.form['password']
    if len(bar) < 1:
        if len(bur) < 8:
            return render_template('signinpage.html', fail_sign='Пароль и логин слишком короткие')
        else:
            return render_template('signinpage.html', fail_sign="Логин слишком короткий")
    else:
        if len(bur) < 8:
            return render_template('signinpage.html', fail_sign='Пароль слишком короткий')
    from data import db_session
    db_session.global_init("db/users_base.sqlite")
    session = db_session.create_session()
    check = db_session.check_user(bar, bur, session)
    if check == '':
        act_name, act_pass = db_session.add_user(bar, bur, session)
        return render_template('hpage_acc.html', form_name=act_name)
    else:
        return render_template('signinpage.html', fail_sign=check)


@app.route('/get-text2', methods=['GET', 'POST'])  # вход, получение логина и пароля
def you():
    global act_name, act_pass
    check = ''
    bar = request.form['login']
    bur = request.form['password']
    from data import db_session
    db_session.global_init("db/users_base.sqlite")
    session = db_session.create_session()
    check = db_session.check_user(bar, bur, session)
    if check == '':
        check = 'Такого пользователя не существует'
        return render_template('loginpage.html', fail_log=check)
    else:
        act_name = bar
        act_pass = bur
        return render_template('hpage_acc.html', form_name=act_name)


@app.route('/h', methods=['GET', 'POST'])  # просто выход из аккаунта
def h():
    global act_name, act_pass
    act_name = 0
    act_pass = 0
    return render_template('homepage.html')


@app.route('/s', methods=['GET', 'POST'])  # выход в регистрацию
def s():
    global act_name, act_pass
    act_name = 0
    act_pass = 0
    return render_template('signinpage.html', fail_sign='')


@app.route('/l', methods=['GET', 'POST'])  # выход в авторизацию
def lo():
    global act_name, act_pass
    act_name = 0
    act_pass = 0
    return render_template('loginpage.html', fail_log='')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
