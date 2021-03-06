from flask import Flask, render_template, request, url_for, redirect, abort, session
from flask_session import Session
import os
from data import db_session
from data.users import User
from forms.user import *
from data.metad import Metad
from data.product import Product
from data.sellers import Seller
from data.cart import Cart
from data.orders import Order
import datetime
from sqlalchemy import func

db_session.global_init("db/shop.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
sess = Session()


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
        user.name = tuple[0]
        user.email = tuple[1]
        user.phone = tuple[2]
        user.address = tuple[3]
        user.city = tuple[4]
        user.country = tuple[5]
        user.password = tuple[6]
        db_sess.add(user)
        db_sess.commit()
    elif data['type'] == "Seller":
        seller = Seller()
        seller.name = tuple[0]
        seller.email = tuple[1]
        seller.phone = tuple[2]
        seller.address = tuple[3]
        seller.city = tuple[4]
        seller.country = tuple[5]
        seller.password = tuple[6]
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
        a = db_sess.query(User).filter(User.email == email, User.password == password)
        if a.count() != 0:
            a = db_sess.query(User).filter(User.email == email, User.password == password)[0]
            a = [a.custID, a.name]
        else:
            a = []
    elif type == "Seller":
        a = db_sess.query(Seller).filter(Seller.email == email, Seller.password == password)
        if a.count() != 0:
            a = db_sess.query(Seller).filter(Seller.email == email, Seller.password == password)[0]
            a = [a.sellID, a.name]
        else:
            a = []
    if len(a) == 0:
        return False
    return a


def get_details(userid, type):
    db_sess = db_session.create_session()
    if type == "Customer":
        a = db_sess.query(User).filter(User.custID == userid)[0]
        d = (str(a.custID), a.name, a.email, a.phone, a.address, a.city, a.country)
        a = []
        a.append(d)
        b = []
    elif type == "Seller":
        a = db_sess.query(Seller).filter(Seller.sellID == userid)[0]
        d = (str(a.sellID), a.name, a.email, a.phone, a.address, a.city, a.country)
        a = []
        a.append(d)
        b = db_sess.query(Product.category).filter(Product.sellID == userid).distinct()
        b = [[i[0]] for i in b]
        b = sum(b, [])
    return a, b


def search_users(search, srch_type):
    db_sess = db_session.create_session()
    search = "%"+search+"%"
    if srch_type == "Customer":
        res = db_sess.query(User).filter(User.name.like(search))
        if res.count() != 0:
            res = db_sess.query(User).filter(User.name.like(search))[0]
            res = (res.custID, res.name, res.email, res.phone, res.address, res.city, res.country)
    elif srch_type == "Seller":
        res = db_sess.query(Seller).filter(Seller.name.like(search))
        if res.count() != 0:
            res = db_sess.query(Seller).filter(Seller.name.like(search))[0]
            res = (res.sellID, res.name, res.email, res.phone, res.address, res.city, res.country)
    res = [i for i in res]
    return res


def update_details(data, userid, type):
    db_sess = db_session.create_session()
    if type == "Customer":
        user = db_sess.query(User).filter(User.custID == userid)[0]
        user.phone = data["phone"]
        user.address = data["address"]
        user.city = data["city"]
        user.country = data["country"]
    elif type == "Seller":
        seller = db_sess.query(Seller).filter(Seller.sellID == userid)[0]
        seller.phone = data["phone"]
        seller.address = data["address"]
        seller.city = data["city"]
        seller.country = data["country"]
    db_sess.commit()


def check_password(psswd, userid, type):
    db_sess = db_session.create_session()
    if type == "Customer":
        a = db_sess.query(User).filter(User.custID == userid)[0]
        a = a.password
    elif type == "Seller":
        a = db_sess.query(Seller).filter(Seller.sellID == userid)[0]
        a = a.password
    return psswd == a


def set_password(psswd, userid, type):
    db_sess = db_session.create_session()
    if type == "Customer":
        user = db_sess.query(User).filter(User.custID == userid)[0]
        user.password = psswd
        db_sess.commit()
    elif type == "Seller":
        seller = db_sess.query(Seller).filter(Seller.sellID == userid)[0]
        seller.password = psswd
        db_sess.commit()


def add_product(sellID, data):
    db_sess = db_session.create_session()
    tup = (
           data["name"],
           data["qty"],
           data["category"],
           data["price"],
           data["desc"],
           sellID)
    prod = Product()
    prod.name = tup[0]
    prod.quantity = tup[1]
    prod.category = tup[2]
    prod.cost_price = tup[3]
    prod.sell_price = round(float(tup[3]) * 1.1)
    prod.description = tup[4]
    prod.sellID = tup[5]
    db_sess.add(prod)
    db_sess.commit()


def get_categories(sellID):
    db_sess = db_session.create_session()
    a = db_sess.query(Product.category).filter(Product.sellID == sellID).distinct()
    categories = [i.category for i in a]
    return categories


def my_product_search(sellID, srchBy, category, keyword):
    db_sess = db_session.create_session()
    if srchBy == "???? ??????????????????":
        a = db_sess.query(Product).filter(Product.category == category, Product.sellID == sellID)
        if a.count() != 0:
            res = []
            b = db_sess.query(Product.prodID).filter(Product.category == category, Product.sellID == sellID).all()
            for i in b:
                for j in i:
                    a = db_sess.query(Product).filter(Product.prodID == j)[0]
                    a = (str(j), a.name, str(a.quantity), a.category, str(a.cost_price))
                    res.append(a)
        else:
            res = ''
    elif srchBy == "???? ????????????????":
        a = db_sess.query(Product).filter(
            ((Product.name.like(keyword)) | (Product.description.like(keyword)) | (Product.category.like(keyword))),
            Product.sellID == sellID)
        if a.count() != 0:
            res = []
            b = db_sess.query(Product.prodID).filter(
                ((Product.name.like(keyword)) | (Product.description.like(keyword)) | (Product.category.like(keyword))),
                Product.sellID == sellID).all()
            for i in b:
                for j in i:
                    a = db_sess.query(Product).filter(Product.prodID == j)[0]
                    a = (str(j), a.name, str(a.quantity), a.category, str(a.cost_price))
                    w = [i for i in a]
                    res.append(w)
        else:
            res = ''
    return res


def product_info(id):
    db_sess = db_session.create_session()
    a = db_sess.query(Product).filter(Product.prodID == id)[0]
    b = db_sess.query(Seller).filter(Seller.sellID == Product.sellID)[0]
    a = (a.name, a.quantity, a.category, a.cost_price, a.sell_price, a.sellID, a.description, b.name)
    res = [i for i in a]
    if len(res) == 0:
        return False, res
    return True, res


def update_product(data, id):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter(Product.prodID == id)[0]
    product.name = data['name']
    product.quantity = data['qty']
    product.category = data['category']
    product.cost_price = data['price']
    product.sell_price = round(1.1 * float(data['price']))
    product.description = data['desp']
    db_sess.commit()


def search_products(srchBy, category, keyword):
    db_sess = db_session.create_session()
    if srchBy == "???? ??????????????????":
        a = db_sess.query(Product).filter(Product.category == category, Product.quantity != 0)
        if a.count() != 0:
            res = []
            b = db_sess.query(Product.prodID).filter(Product.category == category, Product.quantity != 0).all()
            for i in b:
                for j in i:
                    a = db_sess.query(Product).filter(Product.prodID == j)[0]
                    a = (str(j), a.name, a.category, str(a.sell_price))
                    w = [i for i in a]
                    res.append(w)
        else:
            res = ''
    elif srchBy == "???? ????????????????":
        a = db_sess.query(Product).filter(((Product.name.like(keyword)) | (Product.description.like(keyword)) | (Product.category.like(keyword))), Product.quantity != 0)
        if a.count() != 0:
            res = []
            b = db_sess.query(Product.prodID).filter(((Product.name.like(keyword)) | (Product.description.like(keyword)) | (Product.category.like(keyword))), Product.quantity != 0).all()
            for i in b:
                for j in i:
                    a = db_sess.query(Product).filter(Product.prodID == j)[0]
                    a = (str(j), a.name, a.category, str(a.sell_price))
                    w = [i for i in a]
                    res.append(w)
        else:
            res = ''
    return res


def get_seller_products(sellID):
    db_sess = db_session.create_session()
    a = db_sess.query(Product).filter(Product.sellID == sellID, Product.quantity != 0)[0]
    a = (a.prodID, a.name, a.category, a.sell_price)
    res = [i for i in a]
    return res


def place_order(prodID, custID, qty):
    db_sess = db_session.create_session()
    ord = Order()
    a = db_sess.query(Product).filter(Product.prodID == prodID)[0]
    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='??????')
    a = (custID, prodID, qty, datetime.datetime.now(tz), a.cost_price * int(qty), a.sell_price * int(qty), 'PLACED')
    ord.custID = a[0]
    ord.prodID = a[1]
    ord.quantity = a[2]
    ord.date = a[3]
    ord.cost_price = a[4]
    ord.sell_price = a[5]
    ord.status = a[6]
    db_sess.add(ord)
    db_sess.commit()


def customer_orders(custID):
    res = []
    db_sess = db_session.create_session()
    o = db_sess.query(Order.orderID, Order.prodID, Product.name, Order.quantity, Order.sell_price, Order.date,
                      Order.status).filter(Order.prodID == Product.prodID, Order.custID == custID,
                                           Order.status != 'RECIEVED').order_by(Order.date.desc()).all()
    if len(o) != 0:
        for i in o:
            res.append(i)
        return res
    else:
        res = ''
        return res


def seller_orders(sellID):
    res = []
    db_sess = db_session.create_session()
    o = db_sess.query(Order.orderID, Order.prodID, Product.name, Order.quantity, Product.quantity, Order.cost_price,
                      Order.date, Order.status).filter(Order.prodID == Product.prodID, Product.sellID == sellID,
                                                       Order.status != 'RECIEVED').order_by(Order.date.desc()).all()
    if len(o) != 0:
        for i in o:
            res.append(i)
        return res
    else:
        res = ''
        return res


def get_order_details(orderID):
    db_sess = db_session.create_session()
    o = db_sess.query(Order).filter(Order.orderID == orderID, Order.prodID == Product.prodID)[0]
    p = db_sess.query(Product).filter(Product.prodID == Order.prodID)[0]
    a = (o.custID, p.sellID, o.status)
    res = [i for i in a]
    return res


def change_order_status(orderID, new_status):
    db_sess = db_session.create_session()
    a = db_sess.query(Order).filter(Order.orderID == orderID)[0]
    a.status = new_status
    if new_status == 'DISPACHED':
        c = db_sess.query(Order).filter(Order.orderID == orderID)[0]
        d = c.quantity
        print(d)
        c = c.prodID
        b = db_sess.query(Product).filter(Product.prodID == c)[0]
        b.quantity = int(str(b.quantity)) - int(str(d))
        print(b.quantity)
    db_sess.commit()


def customer_purchases(custID):
    res = []
    db_sess = db_session.create_session()
    o = db_sess.query(Order.prodID, Product.name, Order.quantity, Order.sell_price,
                      Order.date).filter(Order.prodID == Product.prodID, Order.custID == custID,
                                    Order.status == 'RECIEVED').order_by(Order.date.desc()).all()
    if len(o) != 0:
        for i in o:
            res.append(i)
        return res
    else:
        res = ''
        return res



def seller_sales(sellID):
    res = []
    db_sess = db_session.create_session()
    o = db_sess.query(Order.prodID, Product.name, Order.quantity, Order.sell_price, Order.date,
                      Order.custID).filter(Order.prodID == Product.prodID, Order.custID == User.custID,
                                    Order.status == 'RECIEVED').order_by(Order.date.desc()).all()
    if len(o) != 0:
        for i in o:
            res.append(i)
        return res
    else:
        res = ''
        return res


def add_product_to_cart(prodID, custID):
    db_sess = db_session.create_session()
    inse = Cart()
    inse.custID = custID
    inse.prodID = prodID
    inse.quantity = 1
    db_sess.add(inse)
    db_sess.commit()


def get_cart(custID):
    db_sess = db_session.create_session()
    s = db_sess.query(Cart.prodID, func.sum(Cart.quantity)).group_by(Cart.prodID).filter(Cart.custID == custID).all()
    b = []
    if len(s) != 0:
        for i in s:
            j, f = i
            a = db_sess.query(Product).filter(Product.prodID == j)[0]
            a = (a.prodID, a.name, a.sell_price, f, a.quantity)
            b.append(a)
        res = [i for i in b]
        return res
    else:
        res = ''
        return res


def update_cart(custID, qty):
    db_sess = db_session.create_session()
    for prodID in qty:
        d = db_sess.query(Cart).filter(Cart.custID == custID, Cart.prodID == prodID).first()
        db_sess.delete(d)
        cart_up = Cart()
        cart_up.custID = custID
        cart_up.prodID = prodID
        cart_up.quantity = qty[prodID]
        db_sess.add(cart_up)
    db_sess.commit()


def cart_purchase(custID):
    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='??????')
    db_sess = db_session.create_session()
    cart = get_cart(custID)
    for item in cart:
        prodID = item[0]
        qty = item[3]
        prod = db_sess.query(Product).filter(Product.prodID == prodID).first()
        prod = (custID, prodID, qty, prod.cost_price * qty, prod.sell_price * qty)
        purchase = Order()
        purchase.custID = prod[0]
        purchase.prodID = prod[1]
        purchase.quantity = prod[2]
        purchase.date = datetime.datetime.now(tz)
        purchase.cost_price = prod[3]
        purchase.sell_price = prod[4]
        purchase.status = 'PLACED'
        db_sess.add(purchase)
        p = db_sess.query(Cart).filter(Cart.custID == custID, Cart.prodID == prodID)[0]
        db_sess.delete(p)
        db_sess.commit()


def empty_cart(custID):
    db_sess = db_session.create_session()
    emp = db_sess.query(Cart).filter(Cart.custID == custID).delete()
    db_sess.commit()


def remove_from_cart(custID, prodID):
    db_sess = db_session.create_session()
    rem = db_sess.query(Cart).filter(Cart.custID == custID, Cart.prodID == prodID).first()
    db_sess.delete(rem)
    db_sess.commit()


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


@app.route("/signup/", methods=["POST", "GET"])
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


@app.route("/viewprofile/<id>/")
def view_profile(id):
    if 'userid' not in session:
        return redirect(url_for('home'))
    userid = session["userid"]
    type = session["type"]
    if str(userid) == id:
        my = True
    else:
        my = False
    if not my:
        profile_type = "Customer" if type == "Seller" else "Seller"
    else:
        profile_type = type
    det, categories = get_details(id, profile_type)
    if len(det) == 0:
        abort(404)
    det = det[0]
    return render_template("view_profile.html",
                            type=profile_type,
                            name=det[1],
                            email=det[2],
                            phone=det[3],
                            address=det[4],
                            city=det[5],
                            country=det[6],
                            category=(None if profile_type == "Customer" else categories),
                            my=my)


@app.route("/viewprofile/", methods=["POST", "GET"])
def profile():
    if 'userid' not in session:
        return redirect(url_for('home'))
    type = "Seller" if session['type'] == "Customer" else "Customer"
    if request.method == "POST":
        search = request.form['search']
        results = []
        res = search_users(search, type)
        if len(res) != 0:
            results.append(res)
        else:
            results = ''
        found = len(results)
        return render_template('profiles.html', id=session['userid'], type=type, after_srch=True, found=found, results=results)

    return render_template('profiles.html', id=session['userid'], type=type, after_srch=False)


@app.route("/viewprofile/<id>/sellerproducts/")
def seller_products(id):
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session["type"] == "Seller":
        abort(403)
    det, categories = get_details(id, "Seller")
    if len(det) == 0:
        abort(404)
    det = det[0]
    name=det[1]
    res = get_seller_products(id)
    return render_template('seller_products.html', name=name, id=id, results=res)


@app.route("/editprofile/", methods=["POST", "GET"])
def edit_profile():
    if 'userid' not in session:
        return redirect(url_for('home'))

    if request.method == "POST":
        data = request.form
        update_details(data, session['userid'], session['type'])
        return redirect(url_for('view_profile', id=session['userid']))

    if request.method == "GET":
        userid = session["userid"]
        type = session["type"]
        det, _ = get_details(userid, type)
        det = det[0]
        return render_template("edit_profile.html",
                                type=type,
                                name=det[1],
                                email=det[2],
                                phone=det[3],
                                address=det[4],
                                city=det[5],
                                country=det[6])


@app.route("/changepassword/", methods=["POST", "GET"])
def change_password():
    if 'userid' not in session:
        return redirect(url_for('home'))
    check = True
    equal = True
    if request.method == "POST":
        userid = session["userid"]
        type = session["type"]
        old_psswd = request.form["old_psswd"]
        new_psswd = request.form["new_psswd"]
        cnfrm_psswd = request.form["cnfrm_psswd"]
        check = check_password(old_psswd, userid, type)
        if check:
            equal = (new_psswd == cnfrm_psswd)
            if equal:
                set_password(new_psswd, userid, type)
                return redirect(url_for('home'))
    return render_template("change_password.html", check=check, equal=equal)


@app.route("/sell/", methods=["POST", "GET"])
def my_products():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session["type"] == "Customer":
        abort(403)
    categories = get_categories(session["userid"])
    if request.method == "POST":
        data = request.form
        srchBy = data["?????????? ????????????"]
        category = None if srchBy == '???? ????????????????' else data["category"]
        keyword = data["keyword"]
        results = my_product_search(session['userid'], srchBy, category, keyword)
        return render_template('my_products.html', categories=categories, after_srch=True, results=results)
    return render_template("my_products.html", categories=categories, after_srch=False)


@app.route("/sell/addproducts/", methods=["POST", "GET"])
def add_products():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session["type"] == "Customer":
        abort(403)
    if request.method == "POST":
        data = request.form
        add_product(session['userid'],data)
        return redirect(url_for('my_products'))
    return render_template("add_products.html")


@app.route("/viewproduct/")
def view_prod():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type'] == "Seller":
        return redirect(url_for('my_products'))
    if session['type'] == "Customer":
        return redirect(url_for('buy'))


@app.route("/viewproduct/<id>/")
def view_product(id):
    if 'userid' not in session:
        return redirect(url_for('home'))
    type = session["type"]
    ispresent, tup = product_info(id)
    if not ispresent:
        abort(404)
    (name, quantity, category, cost_price, sell_price, sellID, desp, sell_name) = tup
    if type == "Seller" and sellID != session['userid']:
        abort(403)
    return render_template('view_product.html', type=type, name=name, quantity=quantity, category=category,
                           cost_price=cost_price, sell_price=sell_price, sell_id=sellID, sell_name=sell_name,
                           desp=desp, prod_id=id)


@app.route("/viewproduct/<id>/edit/", methods=["POST", "GET"])
def edit_product(id):
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type'] == "Customer":
        abort(403)
    ispresent, tup = product_info(id)
    if not ispresent:
        abort(404)
    (name, quantity, category, cost_price, sell_price, sellID, desp, sell_name) = tup
    if sellID != session['userid']:
        abort(403)
    if request.method == "POST":
        data = request.form
        update_product(data, id)
        return redirect(url_for('view_product', id=id))
    return render_template('edit_product.html', prodID=id, name=name, qty=quantity, category=category, price=cost_price, desp=desp)


@app.route("/buy/", methods=["POST", "GET"])
def buy():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type'] == "Seller":
        abort(403)
    if request.method == "POST":
        data = request.form
        srchBy = data["?????????? ????????????"]
        category = None if srchBy == '???? ????????????????' else data["category"]
        keyword = data["keyword"]
        results = search_products(srchBy, category, keyword)
        return render_template('search_products.html', after_srch=True, results=results)
    return render_template('search_products.html', after_srch=False)


@app.route("/buy/<id>/", methods=['POST', 'GET'])
def buy_product(id):
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type'] == "Seller":
        abort(403)
    ispresent, tup = product_info(id)
    if not ispresent:
        abort(404)
    (name, quantity, category, cost_price, sell_price, sellID, desp, sell_name) = tup
    if request.method == "POST":
        data = request.form
        total = int(data['qty'])*float(sell_price)
        return redirect(url_for('buy_confirm', total=total, quantity=data['qty'], id=id))
    return render_template('buy_product.html', name=name, category=category, desp=desp, quantity=quantity, price=sell_price)


@app.route("/buy/<id>/confirm/", methods=["POST", "GET"])
def buy_confirm(id):
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type'] == "Seller":
        abort(403)
    ispresent, tup = product_info(id)
    if not ispresent:
        abort(404)
    (name, quantity, category, cost_price, sell_price, sellID, desp, sell_name) = tup
    if 'total' not in request.args or 'quantity' not in request.args:
        abort(404)
    total = request.args['total']
    qty = request.args['quantity']
    if request.method == "POST":
        choice = request.form['choice']
        if choice == "?????????????????????? ??????????":
            place_order(id, session['userid'], qty)
            return redirect(url_for('my_orders'))
        elif choice == "????????????":
            return redirect(url_for('buy_product', id=id))
    items = ((name, qty, total),)
    return render_template('buy_confirm.html', items=items, total=total)


@app.route("/buy/myorders/")
def my_orders():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type'] == "Seller":
        abort(403)
    res = customer_orders(session['userid'])
    return render_template('my_orders.html', orders=res)


@app.route("/cancel/<orderID>/")
def cancel_order(orderID):
    if 'userid' not in session:
        return redirect(url_for('home'))
    res = get_order_details(orderID)
    if len(res) == 0:
        abort(404)
    custID = res[0]
    sellID = res[1]
    status = res[2]
    if session['type'] == "Seller" and sellID != session['userid']:
        abort(403)
    if session['type'] == "Customer" and custID != session['userid']:
        abort(403)
    if status != "PLACED":
        abort(404)
    change_order_status(orderID, "CANCELLED")
    return redirect(url_for('my_orders')) if session['type'] == "Customer" else redirect(url_for('new_orders'))


@app.route("/dispatch/<orderID>/")
def dispatch_order(orderID):
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type'] == "Customer":
        abort(403)
    res = get_order_details(orderID)
    if len(res) == 0:
        abort(404)
    custID = res[0]
    sellID = res[1]
    status = res[2]
    if session['userid'] != sellID:
        abort(403)
    if status != "PLACED":
        abort(404)
    change_order_status(orderID, "DISPACHED")
    return redirect(url_for('new_orders'))


@app.route("/recieve/<orderID>/")
def recieve_order(orderID):
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type'] == "Seller":
        abort(403)
    res = get_order_details(orderID)
    if len(res) == 0:
        abort(404)
    custID = res[0]
    sellID = res[1]
    status = res[2]
    if session['userid'] != custID:
        abort(403)
    if status != "DISPACHED":
        abort(404)
    change_order_status(orderID, "RECIEVED")
    return redirect(url_for('my_purchases'))


@app.route("/buy/purchases/")
def my_purchases():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type'] == "Seller":
        abort(403)
    res = customer_purchases(session['userid'])
    return render_template('my_purchases.html', purchases=res)


@app.route("/sell/neworders/")
def new_orders():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type'] == "Customer":
        abort(403)
    res = seller_orders(session['userid'])
    return render_template('new_orders.html', orders=res)


@app.route("/sell/sales/")
def my_sales():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type'] == "Customer":
        abort(403)
    res = seller_sales(session['userid'])
    return render_template('my_sales.html', sales=res)


@app.route("/buy/cart/", methods=["POST", "GET"])
def my_cart():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type'] == "Seller":
        abort(403)
    cart = get_cart(session['userid'])
    if request.method == "POST":
        data = request.form
        qty = {}
        for i in data:
            if i.startswith("qty"):
                qty[i[3:]] = data[i]
        update_cart(session['userid'], qty)
        return redirect("/buy/cart/confirm/")
    return render_template('my_cart.html', cart=cart)


@app.route("/buy/cart/confirm/", methods=["POST", "GET"])
def cart_purchase_confirm():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type'] == "Seller":
        abort(403)
    if request.method == "POST":
        choice = request.form['choice']
        if choice == "?????????????????????? ??????????":
            cart_purchase(session['userid'])
            return redirect(url_for('my_orders'))
        elif choice == "????????????":
            return redirect(url_for('my_cart'))
    cart = get_cart(session['userid'])
    items = [(i[1], i[3], float(i[2])*float(i[3])) for i in cart]
    total = 0
    for i in cart:
        total += float(i[2])*int(i[3])
    return render_template('buy_confirm.html', items=items, total=total)


@app.route("/buy/cart/<prodID>/")
def add_to_cart(prodID):
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type'] == "Seller":
        abort(403)
    add_product_to_cart(prodID, session['userid'])
    return redirect(url_for('view_product', id=prodID))


@app.route("/buy/cart/delete/")
def delete_cart():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['userid'] == "Seller":
        abort(403)
    empty_cart(session['userid'])
    return redirect(url_for('my_cart'))


@app.route("/buy/cart/delete/<prodID>/")
def delete_prod_cart(prodID):
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['userid'] == "Seller":
        abort(403)
    remove_from_cart(session['userid'], prodID)
    return redirect(url_for('my_cart'))


app.config['SESSION_TYPE'] = 'filesystem'
app.config['TEMPLATES_AUTO_RELOAD'] = True
sess.init_app(app)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
