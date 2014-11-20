import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import csv     
import datetime

FILENAME = 'legendinisdb.txt'

app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('LEGENDINIS_SETTINGS', silent=True)
currentmsg="";

def write_db(user, message):
    dt = datetime.datetime.now()
    sdt = dt.strftime('%Y/%m/%d %H:%M:%S')
    with open(FILENAME, "a") as myfile:
      myfile.write(user + ',' + sdt+ ',' + message + "\n");
      myfile.close();

def read_db():
    if os.path.exists(FILENAME):
      db = file(FILENAME, "r+")
    else:
      db = file(FILENAME, "w+")

    
    messagereader = csv.reader(db, delimiter=',')
    list = [];
    for k in messagereader:
        tripple = [k[0], k[1], k[2]]
        list.append(tripple);
    print "I was reading db " + str(len(list))   
    return list;


@app.before_request
def before_request():
    print "request coming in"

"""@app.teardown_request
def teardown_request(exception):    
    if currentmsg is not None:
        write_db("whonows",str(datetime.datetime.now()), currentmsg);
"""

@app.route('/')
def show_entries():
    print "got request to showentries"
    messagedb = read_db()
    count = len(messagedb)
    if (count > 20):
       start = count-20
    else:
       start=0;
    messagedb=messagedb[start:count]
    latestentries = [dict(username=row[0], time=row[1], message=row[2]) for row in messagedb]
    return render_template('show_entries.html', entries=latestentries)


@app.route('/add', methods=['POST'])
def add_entry():
    print "got requestt to add"
    if not session.get('logged_in'):
        abort(401) 
    print "user "  + session['username'] ,  "msg " + request.form['message']
    write_db(session['username'], request.form['message'])
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session['logged_in'] = True
        session['username'] = request.form['username']
        flash('You were logged in')
        return redirect(url_for('show_entries'))
    else: 
        return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))



if __name__ == '__main__':
    app.run()
