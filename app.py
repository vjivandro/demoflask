import os
from flask import Flask, make_response, session, flash, abort, redirect
from flask.globals import request
from flask import Flask, render_template
from flask.helpers import url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'randomstring'

@app.errorhandler(401)
def page_not_found(e):
    return render_template('401.html'), 401

@app.route('/')
def hello():
    search = request.args.get('search')
    return render_template('index.html', search=search)

@app.route('/profile/<username>')
def show_profile(username):
    return render_template('profile.html', username=username)

@app.route('/login', methods=['GET','POST'])
def show_login():
    if request.method == 'POST':
        # resp = make_response('Email kamu adalah ' + request.form['email'])
        # resp.set_cookie('email_user', request.form['email'])

        if request.form['password'] == '':
            abort(401)
            
        session['username'] = request.form['email']
        flash('Anda berhasil login!', 'success')
        return redirect(url_for('show_profile', username=session['username']))

    if 'username' in session:
        username = session['username']
        return redirect(url_for('show_profile', username=username))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('show_login'))


@app.route('/getcookie')
def getCookie():
    email = request.cookies.get('email_user')
    return 'Email yang tersimpan di cookie adalah ' + email


ALLOWED_EXTENSION = set(['png','jpeg','jpg'])
app.config['UPLOAD_FOLDER'] = 'uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSION

@app.route('/uploadfile', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        file = request.files['file']

        if 'file' not in request.files:
            return redirect(request.url)
        
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file sudah berhasil disimpan' + filename
            
    return render_template('upload.html')
