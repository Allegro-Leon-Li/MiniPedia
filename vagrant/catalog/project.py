from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Udacity Project"

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

HOME_ITEM_COUNT = 10

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])


@app.route('/catalog/<int:category_id>/JSON')
def categoryJSON(category_id):
    items = session.query(CategoryItem).filter(CategoryItem.category_id == category_id).all()
    return jsonify(Items=[c.serialize for c in items])


@app.route('/catalog/item/<int:item_id>/JSON')
def itemJSON(item_id):
    item = session.query(CategoryItem).filter(CategoryItem.id == item_id).one()
    return jsonify(ItemContent=item.serialize)


@app.route('/')
def catalog():
    categories = session.query(Category)
    items = []
    for i in session.query(CategoryItem).order_by(CategoryItem.id):
        items.append(i)
    limit = len(items) if len(items) < HOME_ITEM_COUNT else HOME_ITEM_COUNT
    items = items[0:limit]
    return render_template(
        'index.html', categories=categories, items=items)


@app.route('/catalog/<string:name>/Items')
def categoryItems(name):
    categories = session.query(Category)
    curr = session.query(Category).filter_by(name=name).one()
    items = session.query(CategoryItem).filter_by(category_id=curr.id)
    return render_template(
        'items.html', categories=categories, items=items)


@app.route('/catalog/<string:categoryname>/<string:itemname>')
def showItem(categoryname, itemname):
    categories = session.query(Category)
    curr = session.query(Category).filter_by(name=categoryname).one()
    item = session.query(CategoryItem).filter_by(name=itemname).filter_by(category_id=curr.id).one()
    return render_template(
        'content.html', item=item)


# @app.route('/restaurants/<int:category_id>/new', methods=['GET', 'POST'])
# def newCategoryItem(category_id):

#     if request.method == 'POST':
#         # newItem = CategoryItem(name=request.form['name'], description=request.form[
#         #                    'description'], price=request.form['price'], course=request.form['course'], category_id=category_id)
#         newItem = CategoryItem(
#             name=request.form['name'], category_id=category_id)
#         session.add(newItem)
#         session.commit()
#         return redirect(url_for('restaurantMenu', category_id=category_id))
#     else:
#         return render_template('newmenuitem.html', category_id=category_id)


@app.route('/catalog/<string:item_name>/edit',
           methods=['GET', 'POST'])
def editCategoryItem(item_name):
    editedItem = session.query(CategoryItem).filter_by(name=item_name).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            # category_id = request.form['category']
            # categories = session.query(Category).filter_by(id=category_id)
            editedItem.category_id = request.form['category']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('catalog'))
    else:
        categories = session.query(Category)
        return render_template(
            'edititem.html', item=editedItem, categories=categories)


@app.route('/catalog/<string:item_name>/delete',
           methods=['GET', 'POST'])
def deleteCategoryItem(item_name):
    itemToDelete = session.query(CategoryItem).filter_by(name=item_name).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('catalog'))
    else:
        return render_template('deleteitem.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)