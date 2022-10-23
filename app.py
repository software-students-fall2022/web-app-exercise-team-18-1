#!/usr/bin/env python3

from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import dotenv_values

import pymongo
import datetime
from bson.objectid import ObjectId
import sys
# from flask_simplelogin import SimpleLogin

# instantiate the app
app = Flask(__name__)


# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
config = dotenv_values(".env")
# turn on debugging if in development mode
if config['FLASK_ENV'] == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode


# connect to the database
cxn = pymongo.MongoClient(config['MONGO_URI'], serverSelectionTimeoutMS=5000)
try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    db = cxn[config['MONGO_DBNAME']] # store a reference to the database
    print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!
except Exception as e:
    # the ping command failed, so the connection is not available.
    # render_template('error.html', error=e) # render the edit template
    print(' *', "Failed to connect to MongoDB at", config['MONGO_URI'])
    print('Database connection error:', e) # debug

# connection = pymongo.MongoClient("localhost", 27017,
#                                 username="admin",
#                                 password="secret",
#                                 authSource="example")
# # select a specific database on the server
# db = connection["example"]

# set up the routes

# route for the home page
@app.route('/')
def home():
    """
    Route for the home page
    """
    docs = db.exampleapp.find({}).sort("created_at", -1) # sort in descending order of created_at timestamp
    return render_template('index.html', docs=docs) # render the hone template


@app.route('/home', methods=['POST'])
def get_home():
    username = request.form['username']
    password = request.form['password']

    user = db.users.find_one({
        "username": username,
        "password": password
    })

    if(user == None):
        return redirect(url_for('login'))
    elif(user['is_business'] == 1):
        return redirect(url_for('bus_home'))
    else:
        return redirect(url_for('cus_home'))

@app.route('/home/<uid>')
    


# route to accept form submission and create a new post
@app.route('/create', methods=['POST'])
def create_post():
    """
    Route for POST requests to the create page.
    Accepts the form submission data for a new document and saves the document to the database.
    """
    name = request.form['fname']
    message = request.form['fmessage']


    # create a new document with the data the user entered
    doc = {
        "name": name,
        "message": message, 
        "created_at": datetime.datetime.utcnow()
    }
    db.exampleapp.insert_one(doc) # insert a new document

    return redirect(url_for('home')) # tell the browser to make a request for the / route (the home function)


# route to view the edit form for an existing post
@app.route('/edit/<mongoid>')
def edit(mongoid):
    """
    Route for GET requests to the edit page.
    Displays a form users can fill out to edit an existing record.
    """
    doc = db.exampleapp.find_one({"_id": ObjectId(mongoid)})
    return render_template('edit.html', mongoid=mongoid, doc=doc) # render the edit template


# route to accept the form submission to delete an existing post
@app.route('/edit/<mongoid>', methods=['POST'])
def edit_post(mongoid):
    """
    Route for POST requests to the edit page.
    Accepts the form submission data for the specified document and updates the document in the database.
    """
    name = request.form['fname']
    message = request.form['fmessage']

    doc = {
        # "_id": ObjectId(mongoid), 
        "name": name, 
        "message": message, 
        "created_at": datetime.datetime.utcnow()
    }

    db.exampleapp.update_one(
        {"_id": ObjectId(mongoid)}, # match criteria
        { "$set": doc }
    )

    return redirect(url_for('home')) # tell the browser to make a request for the / route (the home function)

# route to delete a specific post
@app.route('/delete/<mongoid>')
def delete(mongoid):
    """
    Route for GET requests to the delete page.
    Deletes the specified record from the database, and then redirects the browser to the home page.
    """
    db.exampleapp.delete_one({"_id": ObjectId(mongoid)})
    return redirect(url_for('home')) # tell the web browser to make a request for the / route (the home function)



@app.route('/home/customer/', methods=['GET', 'POST'])
def customer_home():
    docs = db.reviews.find({}).sort("created_at", -1) 
    return render_template('customer_home.html', docs=docs)

@app.route('/home/customer/truck', methods=['GET', 'POST'])
def view_truck():
    docs = db.trucks.find({}).sort("created_at", -1)
    return render_template('view_trucks.html', docs=docs)

####################
# login and register
####################


@app.route('/register/customer/', methods=['POST', 'GET'])
def register_customer():
    if request.method == 'GET':
        return render_template('register_customer.html')
    else:
        email = str(request.form.get('email')).replace(".", "_")
        password = request.form.get('password')
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        if db.customers.count({"email": email}) > 0:
            return render_template('register_customer.html', error='User already exists!')

        elif len(email) >= 50 or len(email.split("@")) < 2:
            return render_template('register_customer.html', error='Please enter a valid email!')

        elif len(name) >= 50:
            return render_template('register_customer.html', error='Your name is too long!')

        elif len(phone_number) > 13:
            return render_template('register_customer.html', error='Please enter a real phone number!')

        else:
            try:
                int_phone_number = int(phone_number)
            except:
                return render_template('register_customer.html', error='Please enter a real phone number!')


            # md5_pass = md5(password.encode('utf-8')).hexdigest()
            # new_id = mt.root_new_user_gen_id(user='root')
            db.customers.insert({
                "email": email,
                "password": password,
                "name": name,
                "phone_number": phone_number,
                });         
            return home()


@app.route('/register/owner/', methods=['POST', 'GET'])
def register_owner():
    if request.method == 'GET':
        return render_template('register_owner.html')
    else:
        email = str(request.form.get('email')).replace(".", "_")
        password = request.form.get('password')
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')


        if db.owners.count({"email": email}) > 0:
            return render_template('register_owner.html', error='User already exists!')

        elif len(email) >= 50 or len(email.split("@")) < 2:
            return render_template('register_owner.html', error='Please enter a valid email!')

        elif len(name) >= 50:
            return render_template('register_owner.html', error='Your name is too long!')

        elif len(phone_number) > 13:
            return render_template('register_owner.html', error='Please enter a real phone number!')

        else:
            try:
                int_phone_number = int(phone_number)
            except:
                return render_template('register_owner.html', error='Please enter a real phone number!')


            # md5_pass = md5(password.encode('utf-8')).hexdigest()
            # new_id = mt.root_new_user_gen_id(user='root')
            db.owners.insert({
                "email": email,
                "password": password,
                "name": name,
                "phone_number": phone_number,
                "address": address,

                });         
            return home()


# Login

@app.route('/login/', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        if request.form.get('customer'):
            return login_customer(email=request.form.get('email'), password=request.form.get('password'))
        if request.form.get('owner'):
            return login_owner(email=request.form.get('email'), password=request.form.get('password'))

def login_customer(email, password):

    email = str(email).replace(".", "_")
    print(db.customers.count({"email": email}))
    print(db.customers.find({"email": email}).password)
    if db.customers.count({"email": email}) > 0 and db.customers.find({"email": email}).password == password:
        return render_template('customer_home.html')


    else:
        # login unsuccessful
        return render_template('customer_home.html', error='Wrong username or password!')


def login_owner(email, password):
    email = str(email).replace(".", "_")
    if db.owners.count({"email": email}) > 0 and db.customers.find({"email": email}).password == password:
        return render_template('business_home.html')


    else:
        # login unsuccessful
        return render_template('login.html', error='Wrong username or password!')


#home screen for food truck owners
@app.route('/ft/<ftid>')
def ft_home(ftid):
    doc = db.ft.find_one({"ftid": ftid}) # sort in descending order of created_at timestamp
    return render_template('business_home.html', doc=doc) # render the hone template

@app.route('/ft/<ftid>/menu')
def view_bus_menu(ftid):
    docs = db.menu.find({'ftid': ftid})
    return render_template('view_bus_menu.html', docs=docs)

@app.route('/ft/<ftid>/reviews')
def view_bus_rev(ftid):
    docs = db.reviews.find({'ftid': ftid})
    return render_template('view_bus_reviews.html', docs=docs)

@app.route('/ft/<ftid>/menu/add', methods=['GET', 'POST'])
def add_item(ftid):
    if(request.method == 'GET'):
        return render_template('add_item.html')
    else:
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        calories = request.form['calories']

        doc = {
            'ftid': ftid,
            'name': name,
            'description': description,
            'price': price,
            'calories': calories
        }

        db.menu.insert_one(doc)

        return redirect(url_for('view_bus_menu'))

# how are menu items being stored / how are we grouping them so that they are attached to a given ft
@app.route('/ft/<ftid>/menu/edit', methods=['GET', 'POST'])
def edit_menu(mongoid):
    doc = db.menu.find_one({'_id': ObjectId(mongoid)})

    if(request.method == 'GET'):
        return render_template('edit_item.html', doc=doc)
    else:
        name = doc['name']
        description = doc['description']
        price = doc['price']
        calories = doc['calories']

        if(request.form['name'] != None):
            name = request.form['name']
        if(request.form['description'] != None):
            description = request.form['description']
        if(request.form['price'] != None):
            price = request.form['price']
        if(request.form['calories'] != None):
            calories = request.form['calories']

        new_doc = {
            'name': name,
            'description': description,
            'price': price,
            'calories': calories
        }

        db.menu.update_one(
            {'_id': ObjectId(mongoid)},
            {'$set': new_doc}
        )

        return redirect(url_for('view_bus_menu'))

@app.route('/ft/<ftid>/menu/delete')
def delete_menu_item(mongoid):
    db.menu.delete_one({'_id': ObjectId(mongoid)})
    return redirect(url_for('view_bus_menu'))
        

@app.route('/ft/<ftid>/edit', methods=['GET', 'POST'])
def edit_info(ftid):
    doc = db.ft.find_one({"ftid": ftid})

    if(request.method == 'GET'):
        return render_template('edit_info.html', doc=doc)
    else:
        orig_doc = db.ft.find_one({"ftid": ftid})

        location = orig_doc['location']
        open_time = orig_doc['open_time']
        close_time = orig_doc['close_time']

        if(request.form['location'] != None):
            location = request.form['location']
        if(request.form['open_time'] != None):
            open_time = request.form['open_time']
        if(request.form['close_time'] != None):
            close_time = request.form['close_time']

        new_doc = {
            'location': location,
            'open_time': open_time,
            'close_time': close_time
        }

        db.ft.update_one(
            {'ftid': ftid},
            {'$set': new_doc}
        )

        return redirect(url_for('ft_home'))

#Adding menu items for restaurant owners
@app.route('/ft/<ftid>/add',methods=['POST'])
def menu_add(ftid):
    name = request.form['fname']
    desc = request.form['fdesc']
    price = request.form['fprice']

    doc = {
        # "_id": ObjectId(mongoid), 
        "name": name, 
        "desc": desc, 
        "price": price,
        "is_item": 1,
        "is_hrs": 0,
        "is_rev": 0,
        "is_loc": 0
    }

    # db.ftid.insert_one(doc)
    return redirect

#deleting menu items
@app.route('/ft/<ftid>/delete/<itemid>')
def delete_item(itemid):   
    db.ftid.delete_one({"_id": ObjectId(itemid)})
    return redirect(url_for('home')) # tell the web browser to make a request for the / route (the home function)

#updating menu items
@app.route('/ft/<ftid>/edit/<itemid>', methods=['POST'])
def edit_item(itemid):
 
    name = request.form['fname']
    desc = request.form['fdesc']
    price = request.form['fprice']

    doc = {
        # "_id": ObjectId(mongoid), 
        "name": name, 
        "desc": desc, 
        "price": price,
        "is_item": 1,
        "is_hrs": 0,
        "is_rev": 0,
        "is_loc": 0
    }

    # db.ftid.update_one(
    #     {"_id": ObjectId(itemid)}, # match criteria
    #     { "$set": doc }
    # )

    return redirect(url_for('home')) # tell the browser to make a request for the / route (the home function)

#Changing availability

@app.route('/ft/<ftid>/update/<avid>', methods=['POST'])
def update_avai(avid):
 
    from_x = request.form['from']
    to_x = request.form['to']
    
    #maybe add error handling here
    
    doc = {
        # "_id": ObjectId(mongoid), 
        "from": from_x, 
        "to": to_x,
        "is_item": 0,
        "is_hrs": 1,
        "is_rev": 0,
        "is_loc": 0
    }

    # db.ftid.update_one(
    #     {"_id": ObjectId(avid)}, # match criteria
    #     { "$set": doc }
    # )

    return home() # tell the browser to make a request for the / route (the home function)


#Adding photos


#User browsing restaurants

@app.route('/u/<uid>/<ftid>')
def browse_restaurants():
    items = db.ftid.find({}) # sort in descending order of created_at timestamp
    revs= db.ftid.find({})
    open_hrs = db.v
    return render_template('food_truck.html', items=items, revs=revs, ) # render the hone template






# route to handle any errors
@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template('error.html', error=e) # render the edit template


# run the app
if __name__ == "__main__":
    #import logging
    #logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(debug = True)
