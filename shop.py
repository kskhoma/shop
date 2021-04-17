from flask import Flask, render_template, request, url_for, redirect, abort, session
from flask_session import Session
import os
from data import db_session
from data.users import User
from forms.user import *
from data.metad import Metad
from data.product import Product
from data.sellers import Seller


db_session.global_init("db/shop.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
sess = Session()


def custID_generation():
    db_sess = db_session.create_session()
    customer_num = db_sess.query(Metad)
    customer_num.customer_num = int(customer_num) + 1
    db_sess.commit()
    customer_num = str([i for i in db_sess.query(Metad).customer_num][0][0])
    id = "CID" + "0" * (7 - len(customer_num)) + customer_num
    return id


def sellIID_generation():
    db_sess = db_session.create_session()
    seller_num = db_sess.query(Metad)
    seller_num.seller_num = int(seller_num) + 1
    db_sess.commit()
    seller_num = str([i for i in db_sess.query(Metad).seller_num][0][0])
    id = "SID" + "0" * (7 - len(seller_num)) + seller_num
    return id


def new_user(data):
    db_sess = db_session.create_session()
    email = data["email"]
    if data['type'] == "Customer":
        a = db_sess.query(User).filter(User.email == email)
    elif data['type'] == "Seller":
        a = db_sess.query(Seller).filter(Seller.email == email)
    if len(list(a)) != 0:
        return False
    tuple = ( data["name"],
            data["email"],
            data["phone"],
            data["address"],
            data["city"],
            data["country"],
            data["password"])
    if data['type'] == "Customer":
        user = User()
        user.id = custID_generation()
        user.name = tuple[0]
        user.email = tuple[1]
        user.address = tuple[2]
        user.city = tuple[3]
        user.country = tuple[4]
        user.password = tuple[5]
        db_sess.add(user)
        db_sess.commit()
    elif data['type'] == "Seller":
        seller = Seller()
        seller.id = custID_generation()
        seller.name = tuple[0]
        seller.email = tuple[1]
        seller.address = tuple[2]
        seller.city = tuple[3]
        seller.country = tuple[4]
        seller.password = tuple[5]
        db_sess.add(seller)
        db_sess.commit()
    db_sess.commit()
    return True


def authorization(data):
    db_sess = db_session.create_session()
    type = data["type"]
    email = data["email"]
    password = data["password"]
    if type == "Customer":
        a = db_sess.query(User).filter(User.email == email, User.password == password)[0]
        a = [a.custID, a.name]
    elif type == "Seller":
        a = db_sess.query(Seller).filter(Seller.email == email, Seller.password == password)[0]
        a = [a.sellID, a.name]
    if len(a) == 0:
        return False
    return a[0]


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.form
        user_inf = authorization(data)
        if user_inf:
            session["userid"] = user_inf[0]
            session["name"] = user_inf[1]
            session["type"] = data["type"]
            return redirect(url_for('home'))
        return render_template("login.html", err=True)
    return render_template("login.html", err=False)


@app.route("/logout/")
def logout():
    session.pop('userid')
    session.pop('name')
    session.pop('type')
    return redirect(url_for('home'))


@app.route("/signup/", methods = ["POST", "GET"])
def signup():
    if request.method == "POST":
        data = request.form
        ok = new_user(data)
        if ok:
            return render_template("success_signup.html")
        return render_template("signup.html", ok=ok)
    return render_template("signup.html", ok=True)


@app.route("/")
def home():
    if "userid" in session:
        return render_template("home.html", signedin=True, id=session['userid'], name=session['name'], type=session['type'])
    return render_template("home.html", signedin=False)


app.config['SESSION_TYPE'] = 'filesystem'
app.config['TEMPLATES_AUTO_RELOAD'] = True
sess.init_app(app)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')