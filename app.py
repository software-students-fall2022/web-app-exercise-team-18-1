#!/usr/bin/env python3

#from crypt import methods
#from crypt import methods
from operator import methodcaller
from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import dotenv_values

import pymongo
import datetime
from bson.objectid import ObjectId
import sys
#from flask_simplelogin import SimpleLogin

# instantiate the app
app = Flask(__name__)
#SimpleLogin(app)

# app.new_ftid = 0
# app.new_csid = 0

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
@app.route('/<uid>/')
def home(uid):
    """
    Route for the home page after login
    """
    doc = db.users.find_one({'username': uid}) # sort in descending order of created_at timestamp
    if(doc['is_owner'] == 0):
        return redirect(url_for('cs_home', csid=uid, uid=uid))
    else:
        return redirect(url_for('ft_home', ftid=uid, uid=uid)) # render the hone template

@app.route('/')
def index():
    return redirect(url_for('login'))

# @app.route('/login')
# def login():
#     return render_template('login.html')

# @app.route('/home/', methods=['POST'])
# def get_home():
#     username = request.form['username']
#     password = request.form['password']

#     user = db.users.find_one({
#         "username": username,
#         "password": password
#     })

#     if(user == None):
#         return redirect(url_for('login'))
#     elif(user['is_business'] == 1):
#         return redirect(url_for('bus_home'))
#     else:
#         return redirect(url_for('cus_home'))



# route to accept form submission and create a new post
# @app.route('/create', methods=['POST'])
# def create_post():
#     """
#     Route for POST requests to the create page.
#     Accepts the form submission data for a new document and saves the document to the database.
#     """
#     name = request.form['fname']
#     message = request.form['fmessage']


#     # create a new document with the data the user entered
#     doc = {
#         "name": name,
#         "message": message, 
#         "created_at": datetime.datetime.utcnow()
#     }
#     db.exampleapp.insert_one(doc) # insert a new document

#     return redirect(url_for('home')) # tell the browser to make a request for the / route (the home function)


# route to view the edit form for an existing post
# @app.route('/edit/<mongoid>')
# def edit(mongoid):
#     """
#     Route for GET requests to the edit page.
#     Displays a form users can fill out to edit an existing record.
#     """
#     doc = db.exampleapp.find_one({"_id": ObjectId(mongoid)})
#     return render_template('edit.html', mongoid=mongoid, doc=doc) # render the edit template


# route to accept the form submission to delete an existing post
# @app.route('/edit/<mongoid>', methods=['POST'])
# def edit_post(mongoid):
#     """
#     Route for POST requests to the edit page.
#     Accepts the form submission data for the specified document and updates the document in the database.
#     """
#     name = request.form['fname']
#     message = request.form['fmessage']

#     doc = {
#         # "_id": ObjectId(mongoid), 
#         "name": name, 
#         "message": message, 
#         "created_at": datetime.datetime.utcnow()
#     }

#     db.exampleapp.update_one(
#         {"_id": ObjectId(mongoid)}, # match criteria
#         { "$set": doc }
#     )

#     return redirect(url_for('home')) # tell the browser to make a request for the / route (the home function)

# route to delete a specific post
# @app.route('/delete/<mongoid>')
# def delete(mongoid):
#     """
#     Route for GET requests to the delete page.
#     Deletes the specified record from the database, and then redirects the browser to the home page.
#     """
#     db.exampleapp.delete_one({"_id": ObjectId(mongoid)})
#     return redirect(url_for('home')) # tell the web browser to make a request for the / route (the home function)



####################
# login and register
####################

# @app.route('/sign-up/', methods=['POST', 'GET'])
# def sign_up():
#     if(request.method == 'GET'):
#         return render_template('sign_up.html')
#     else:
#         username = request.form['username']
#         password = request.form['password']
#         try:
#             is_owner = request.form['is_owner']
#         except:
#             is_owner = 'off'

#         if(is_owner == 'on'):
#             doc = {
#                 'username': username,
#                 'password': password,
#                 'is_owner': is_owner,
#                 'ftid': app.new_ftid
#             }

#             db.users.insert_one(doc)

#             return redirect(url_for('bus_sign_up'))
#         else:
#             doc = {
#                 'username': username,
#                 'password': password,
#                 'is_owner': is_owner,
#                 'csid': app.new_csid
#             }

#             db.users.insert_one(doc)
            
#             new_cs = {
#                 'csid': app.new_csid
#             }
#             app.new_csid = app.new_csid+1

#             db.cs.insert_one(new_cs)

#             return redirect(url_for('login'))

# @app.route('/sign-up/business/', methods=['POST', 'GET'])
# def bus_sign_up():
#     if(request.method == 'GET'):
#         return render_template('sign_up_bus.html')
#     else:
#         name = request.form['name']
#         location = request.form['location']
#         open_time = request.form['open_time']
#         close_time = request.form['close_time']

#         doc = {
#             'ftid': app.new_ftid,
#             'name': name,
#             'location': location,
#             'open_time': open_time,
#             'close_time': close_time,
#             'avg_rating': 0
#         }

#         app.new_ftid = app.new_ftid+1

#         db.ft.insert_one(doc)

#         return redirect(url_for('login'))

@app.route('/register/customer/', methods=['POST', 'GET'])
def register_customer():
    if request.method == 'GET':
        return render_template('register_customer.html')
    else:
        username = str(request.form.get('username')).replace(".", "_")
        password = request.form.get('password')
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        if db.users.count({"username": username}) > 0:
            return render_template('register_customer.html', error='User already exists!')

        elif len(username) >= 50 or len(username.split("@")) < 2:
            return render_template('register_customer.html', error='Please enter a valid username!')

        elif len(name) >= 50:
            return render_template('register_customer.html', error='Your name is too long!')

        elif len(phone_number) > 13:
            return render_template('register_customer.html', error='Please enter a real phone number!')

        else:
            try:
                int(phone_number)
            except:
                return render_template('register_customer.html', error='Please enter a real phone number!')


            # md5_pass = md5(password.encode('utf-8')).hexdigest()
            # new_id = mt.root_new_user_gen_id(user='root')
            db.users.insert({
                "username": username,
                "password": password,
                "name": name,
                "phone_number": phone_number,
                "is_owner": 0,
                });         
            return redirect(url_for('cs_home', csid=username, uid=username))


@app.route('/register/owner/', methods=['POST', 'GET'])
def register_owner():
    if request.method == 'GET':
        return render_template('register_owner.html')
    else:
        username = str(request.form.get('username')).replace(".", "_")
        password = request.form.get('password')
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')

        ft_name = request.form.get('ft_name')
        location = request.form.get('location')
        open_time = request.form.get('open_time')
        close_time = request.form.get('close_time')


        if db.users.count({"username": username}) > 0:
            return render_template('register_owner.html', error='User already exists!')

        elif len(username) >= 50 or len(username.split("@")) < 2:
            return render_template('register_owner.html', error='Please enter a valid username!')

        elif len(name) >= 50:
            return render_template('register_owner.html', error='Your name is too long!')

        elif len(phone_number) > 13:
            return render_template('register_owner.html', error='Please enter a real phone number!')

        else:
            try:
                int(phone_number)
            except:
                return render_template('register_owner.html', error='Please enter a real phone number!')


            # md5_pass = md5(password.encode('utf-8')).hexdigest()
            # new_id = mt.root_new_user_gen_id(user='root')
            db.users.insert({
                "username": username,
                "password": password,
                "name": name,
                "phone_number": phone_number,
                "is_owner": 1
            })
            db.food_trucks.insert({
                "ftid": username,
                "name": ft_name,
                "location": location,
                "open_time": open_time,
                "close_time": close_time,
            }) 
            return redirect(url_for('ft_home', ftid=username, uid=username))


# Login

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        if request.form.get('customer'):
            return login_customer(username=request.form.get('username'), password=request.form.get('password'))
        if request.form.get('owner'):
            return login_owner(username=request.form.get('username'), password=request.form.get('password'))

def login_customer(username, password):

    username = str(username).replace(".", "_")
    if db.users.count({"username": username}) > 0 and db.users.find_one({"username": username})["password"] == password:
        return redirect(url_for('cs_home', csid=username, uid=username))


    else:
        # login unsuccessful
        return render_template('login.html', error='Wrong username or password!')

def login_owner(username, password):
    username = str(username).replace(".", "_")
    if db.users.count({"username": username}) > 0 and db.users.find_one({"username": username})["password"] == password:
        return  redirect(url_for('ft_home', ftid=username, uid=username))


    else:
        # login unsuccessful
        return render_template('login.html', error='Wrong username or password!')


##########################
#      food trucks
##########################

#home screen for food truck owners
@app.route('/ft/<ftid>/')
def ft_home(ftid):
    
    revs=db.reviews.find({"ftid":ftid})
    sumx=0
    num=0
    for r in revs:
        sumx+=int(r['rating'])
        num+=1
    if num==0:
        num=1
        sumx=3
    avg= float(sumx/num)
    db.food_trucks.update_one({"ftid":ftid},{'$set':{'avg_rating': avg}})
    doc = db.food_trucks.find_one({"ftid": ftid}) #find details of the food truck
    return render_template('business_home.html', doc=doc, ftid=ftid) # render the home template

#adding items to menu for a food truck
@app.route('/ft/<ftid>/menu/add/', methods=['GET', 'POST'])
def add_items(ftid):
    if(request.method == 'GET'):
        return render_template('add_item.html', ftid=ftid)
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
            'calories': calories,
        }

        db.menu.insert_one(doc)

        return redirect(url_for('view_bus_menu',ftid=ftid))

#viewing menu for a food truck
@app.route('/ft/<ftid>/menu/')
def view_bus_menu(ftid):
    docs = db.menu.find({'ftid': ftid})
    return render_template('view_bus_menu.html', docs=docs, ftid=ftid)


#viewing reviews for a food truck
@app.route('/ft/<ftid>/reviews/')
def view_bus_rev(ftid):
    docs = db.reviews.find({'ftid': ftid})
    return render_template('view_bus_reviews.html', docs=docs)


@app.route('/ft/<ftid>/menu/<name>/edit/', methods=['GET', 'POST'])
def edit_menu(ftid,name):
    doc = db.menu.find_one({'ftid': ftid, "name":name})


    if(request.method == 'GET'):
        return render_template('edit_item.html', doc=doc, ftid=ftid, name =name)
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
            {'ftid':ftid,'name': doc['name']},
            {'$set': new_doc}
        )

        return redirect(url_for('view_bus_menu',ftid=ftid))

@app.route('/ft/<ftid>/menu/<name>/delete/')
def delete_menu_item(ftid,name):
    db.menu.delete_one({'ftid': ftid, 'name':name})
    return redirect(url_for('view_bus_menu',ftid=ftid))
        

@app.route('/ft/<ftid>/edit/', methods=['GET', 'POST'])
def edit_info(ftid):
    doc = db.food_trucks.find_one({"ftid": ftid})

    if(request.method == 'GET'):
        return render_template('edit_info.html', doc=doc, ftid=ftid)
    else:
        orig_doc = db.food_trucks.find_one({"ftid": ftid})

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

        db.food_trucks.update_one(
            {'ftid': ftid},
            {'$set': new_doc}
        )


        return redirect(url_for('ft_home', ftid=ftid))


#################################
#           CUSTOMERS
#################################

# @app.route('/home/customer/', methods=['GET', 'POST'])
# def customer_home():
#     docs = db.reviews.find({}).sort("created_at", -1) 
#     return render_template('customer_home.html', docs=docs)

@app.route('/cs/<csid>/home')
def cs_home(csid):
    recent_review = db.reviews.find_one({'username': csid})
    print(recent_review, csid)
    return render_template('customer_home.html', recent_review=recent_review, csid=csid, uid=csid)

@app.route('/cs/<csid>/browse/reviews/')
def view_reviews_by_user(csid):
    docs = db.reviews.find({'username': csid})
    return render_template('view_cus_reviews.html', docs=docs, csid=csid, uid=csid)

@app.route('/cs/<csid>/browse/trucks/', methods=['GET', 'POST'])
def browse_trucks(csid):
    if(request.method == 'POST'):
        try:
            sort_highest = request.form['highest_rated']
        except:
            sort_highest = 'off'

        try:
            curr_open = request.form['curr_open']
        except:
            curr_open = 'off'

        if(sort_highest == 'on'):
            if(curr_open == 'on'):
                curr_time = datetime.datetime.now()
                time_parse = curr_time.strftime('%H:%M:%S')

                if(request.form['search_name'] != ''):
                    query = {
                        'name': request.form['search_name'],
                        'open_time': {'$lt': time_parse},
                        'close_time': {'$gt': time_parse}
                    }
                else:
                    query = {
                        'open_time': {'$lt': time_parse},
                        'close_time': {'$gt': time_parse}
                    }

                docs = db.ft.find(query).sort('avg_rating', -1)
            else:
                if(request.form['search_name'] != ''):
                    docs = db.ft.find({'name': request.form['search_name']}).sort('avg_rating', -1)
                else:
                    docs = db.ft.find().sort('avg_rating', -1)
            
            return render_template('view_trucks.html', docs=docs, csid=csid, uid=csid)
        else:
            if(curr_open == 'on'):
                curr_time = datetime.datetime.now()
                time_parse = curr_time.strftime('%H:%M:%S')

                if(request.form['search_name'] != ''):
                    query = {
                        'name': request.form['search_name'],
                        'open_time': {'$lt': time_parse},
                        'close_time': {'$gt': time_parse}
                    }
                else:
                    query = {
                        'open_time': {'$lt': time_parse},
                        'close_time': {'$gt': time_parse}
                    }

                docs = db.ft.find(query)
            else:
                if(request.form['search_name'] != ''):
                    docs = db.ft.find({'name': request.form['search_name']})
                else:
                    docs = db.ft.find()
            
            return render_template('view_trucks.html', docs=docs, csid=csid, uid=csid)
    else:
        docs = db.ft.find()
        # docs["ft"] = db.ft.find()
        # docs["csid"] = csid
        return render_template('view_trucks.html', docs=docs, csid=csid, uid=csid)

# @app.route('/cs/<csid>/add-review/')
# def add_review(mongoid):
#     title = doc['title']
#     description = doc['description']
#     rating = doc['rating']

#     if(request.form['title'] != None):
#         title = request.form['title']
#     if(request.form['description'] != None):
#         description = request.form['description']
#     if(request.form['rating'] != None):
#         rating = request.form['rating']

#     new_doc = {
#         'title': title,
#         'description': description,
#         'rating': rating
#     }

#     db.reviews.update_one(
#         {'_id': ObjectId(mongoid)},
#         {'$set': new_doc}
#     )

#     return redirect(url_for('cs_home'))

@app.route('/cs/<csid>/<mongoid>/edit-review/', methods=['GET', 'POST'])
def edit_review(mongoid, csid):
    doc = db.reviews.find_one({'_id': ObjectId(mongoid)})

    ft_name = doc['b_name']
    id = doc['_id']

    if(request.method == 'GET'):
        return render_template('edit_review.html', doc=doc, ft_name=ft_name, mongoid=id, csid=csid, uid=csid)
    else:
        title = doc['title']
        description = doc['description']
        rating = doc['rating']

        if(request.form['title'] != None):
            title = request.form['title']
        if(request.form['description'] != None):
            description = request.form['description']
        if(request.form['rating'] != None):
            rating = request.form['rating']

        new_doc = {
            'title': title,
            'description': description,
            'rating': rating
        }

        db.reviews.update_one(
            {'_id': ObjectId(mongoid)},
            {'$set': new_doc}
        )

        return redirect(url_for('cs_home', uid=csid, csid=csid))

@app.route('/cs/<csid>/<mongoid>/delete-review/')
def delete_review(csid, mongoid):
    db.reviews.delete_one({'_id': ObjectId(mongoid)})
    return redirect(url_for('cs_home', uid=csid, csid=csid))


@app.route('/cs/<csid>/browse/<ftid>/menu/')
def view_menu(csid, ftid):
    ftid = int(ftid)
    ft = db.ft.find_one({'ftid': ftid})
    docs = db.menu.find({'ftid': ftid})
    return render_template('view_cus_menu.html', ft_name=ft['name'], docs=docs, csid=csid, uid=csid)
    # return render_template('view_cus_menu.html')

@app.route('/cs/<csid>/browse/<ftid>/reviews/')
def view_reviews(csid, ftid):
    ftid = int(ftid)
    ft = db.ft.find_one({'ftid': ftid})
    docs = db.reviews.find({'ftid': ftid})
    return render_template('view_cus_reviews_by_truck.html', ft_name=ft['name'], docs=docs, csid=csid, uid=csid)

@app.route('/cs/<csid>/browse/<ftid>/leave-review/', methods=['GET', 'POST'])
def leave_review(ftid, csid):
    ftid = int(ftid)    
    ft = db.ft.find_one({'ftid': ftid})

    if(request.method == 'GET'):
        return render_template('add_review.html', ft_name=ft['name'], ftid=ftid, csid=csid, uid=csid)
    else:
        title = request.form['title']
        description = request.form['description']
        rating = request.form['rating']

        doc = {
            'csid': csid,
            'ftid': ftid,
            'b_name': ft['name'],
            'title': title,
            'description': description,
            'rating': rating
        }

        db.reviews.insert_one(doc)
        revs=db.reviews.find({"ftid":ftid})
        sumx=0
        num=0
        for r in revs:
            sumx+=int(r['rating'])
            num+=1
        avg= float(sumx/num)
        db.ft.update_one({"ftid":ftid},{'$set':{'avg_rating': avg}})
        return redirect(url_for('browse_trucks', csid=csid, uid=csid))


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