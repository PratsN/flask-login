from flask import Flask, render_template, request, session, redirect, url_for, send_file
from pymongo import MongoClient


app = Flask(__name__, template_folder='Templates')
client = MongoClient(
    'mongodb+srv://pratiksha:pratiksha11@cluster0.4mxlvfp.mongodb.net/?retryWrites=true&w=majority')
db = client['flaskuser']
users = db['users']


@app.route('/home/', methods=['GET', 'POST'])
def home():

    if 'name' in session:
        name = session['name']
        email = session['email']
        url = session['link']
        with open('data.txt', 'w') as file:
            file.write(name + '\n')
            file.write(email + '\n')
            file.write(url + '\n')
            send_file('data.txt', as_attachment=True)
        return render_template('dashboard.html', name=name, email=email, url=url)
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        existing_user = users.find_one({'name': name})
        if existing_user is not None and existing_user['password'] == password:
            session['name'] = request.form['name']
            session['email'] = existing_user['email']
            session['link'] = existing_user['link']
            return redirect(url_for('home'))
        return 'User does not exist'
    return render_template('index.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        link = request.form['link']
        password = request.form['password']
        email = request.form['email']
        existing_user = users.find_one({'name': name})
        if existing_user is None:
            users.insert_one({'name': name, 'email': email,
                             'link': link, 'password': password, })
            session['name'] = name
            return redirect(url_for('index'))
        return 'That user already exists!'
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/readfile')
def readfile():
    # open the file in read mode
    with open('data.txt', 'r') as file:
        # read the contents of the file
        file_contents = file.read()

    # return the file contents as a response
    return file_contents


app.config['SECRET_KEY'] = 'secrete_key_12345'

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
