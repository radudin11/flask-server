import re
from urllib.request import Request
from flask import Flask, request, render_template, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# you can use a dict as user/pass database
ALLOWED_USERS = { "admin": "n0h4x0rz-plz", "radu": "1234"}


app = Flask(__name__, static_folder="public")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "sunt gay, Edi"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    # TODO: render the index page using our template
    return render_template("index.html")


# TODO (Task 03 - Authentication)
@app.route("/login.html", methods = ['GET', 'POST'] )
def login():
    error_msg_pass = "Invalid password"
    error_msg_user = "Invalid user"
    #if session['authenticated'] == 1:
    if 'username' in session:
        return redirect("loggedin.html")
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        # TODO: verify credentials and set the session variables
        for usr in ALLOWED_USERS.keys():
            if usr == username:
                if password == ALLOWED_USERS[username]:
                    #session['authenticated'] = 1
                    session['username'] = username
                    return redirect("loggedin.html")
                return render_template("login.html", error_msg=error_msg_pass)
    return render_template("login.html", error_msg=error_msg_user)

@app.route("/logout.html")
def logout():
    # clear authentication status
    #session["authenticated"] = 0
    session.pop('username', None)
    return redirect("/")

# TODO (Task 04 - File Upload)
@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/loggedin.html")
def loggedin():
    return render_template("loggedin.html")

@app.route("/upload.html", methods = ['GET', 'POST'])
def upload():
    if 'username' in session:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return render_template("upload.html")
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect("upload.html")
        return render_template("upload.html")
    return render_template("login.html", error_msg="You have to be logged in")
if __name__ == "__main__":
    loggedin = False
    app.run(debug=True)

