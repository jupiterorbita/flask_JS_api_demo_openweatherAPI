# ROUTING
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.party_model import Party

# ------- CREATE party PAGE ------
@app.route('/parties/new')
def new_party():
    return render_template("party_new.html")

# ------- CREATE METHOD - FORM ACTION -----
@app.route("/parties/create", methods=['post'])
def create_party_form():
    print(f"\n\n request.form ======>> \n{request.form}\n\n")
    
    if not Party.validate(request.form):
        return redirect("/parties/new")
    
    Party.create(request.form)
    return redirect("/dashboard")

#  ----------- READ ONE page ----------
@app.route("/parties/<int:id>")
def show_one_page(id):
    this_party = Party.get_by_id(id)
    return render_template("party_show.html",
                           this_party = this_party)


# ---------- EDIT party page --------------
@app.route("/parties/<int:id>/edit")
def edit_party_page(id):
    this_party = Party.get_by_id(id)
    return render_template("party_edit.html", 
                           this_party = this_party)

# -------- EDIT ACTION FORM --------
@app.route("/parties/update", methods=['post'])
def update_method():
    print("hello update !!!!!!!!!!!!!!!!!!!!!!!!")
    print(request.form)
    if not Party.validate(request.form):
        return redirect(f"/parties/{request.form['id']}/edit")
    
    Party.update(request.form)
    return redirect("/dashboard")