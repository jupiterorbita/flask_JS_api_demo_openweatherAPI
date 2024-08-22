# ROUTING
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.party_model import Party
from flask_bcrypt import Bcrypt  
bcrypt = Bcrypt(app)

# ========== LOGIN REGISTER PAGE ============
@app.route("/")
def home():
    return render_template("index.html")

# =========== REGISTER - METHOD (form action) ====
@app.route("/users/register", methods=['post'])
def user_reg():
    print(f"^^^^^^^^^^^^^^\nrequest.form: {request.form}")
    # BEFORE WE WRITE THE THE DB
    # WE NEED TO V A L I D A T E the form
    if not User.validate(request.form):
        return redirect("/")
    
    # 1. hash the plain text password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # 2. get the data dict ready with the new hashed pw
    user_data = {
        **request.form,
        'password' : pw_hash
    }
    # 3. pass it to the model to create
    user_id = User.create(user_data)
    # how to keep track if someone is logged in?
    # store the user_id of the created user in session 🎒
    session['user_id'] = user_id
    return redirect("/dashboard")


# ============= LOGIN ACTION ================
@app.route("/users/login", methods=['post'])
def user_login():
    print(f"!!!!!!!!!!!x!!!!! \nrequest.form: {request.form}")
    user_in_db = User.get_by_email(request.form['email'])
    # if email is not found
    if not user_in_db:
        flash("invalid credentials", 'login')
        return redirect("/")
    
    # now check the password
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("invalid credentials", 'login')
        return redirect('/')
    
    # if all is good
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")

# ============= DASHBOARD PAGE - RENDER (after login or register actions)
@app.route("/dashboard")
def dashboard():
    # route guard
    if 'user_id' not in session:
        return redirect("/")
    
    logged_user = User.get_by_id(session['user_id'])

    # get all the parties to show
    all_parties = Party.get_all_parties()

    return render_template("dashboard.html",
                           logged_user = logged_user,
                           all_parties = all_parties)

# =========== LOGOUT ============
@app.route("/logout")
def legout_action():
    session.clear()
    return redirect("/")
