from flask import Flask, flash, redirect, render_template, request
from uuid import uuid4

from db.handlers import insert, read
from db.schemas import Contact

app = Flask(__name__)
app.secret_key = uuid4().bytes
route = app.route


@route("/")
def index():
    return redirect("/contacts")


@route("/contacts")
def contacts():
    if not (q := request.args.get("q")):
        contacts = read()
    else:
        conditions = [{"first": {"$eq": q}}, {"last": {"$eq": q}}]
        contacts = read({"$or": conditions})

    return render_template("index.html", contacts=contacts)


@route("/contacts/new", methods=["GET"])
def contacts_new_get():
    return render_template("new.html", contact=Contact())


@route("/contacts/new", methods=["POST"])
def contact_new_post():
    form = request.form
    new_contact = Contact(**form.to_dict())
    if insert(new_contact):
        flash("Contact added successfully!", "success")
        return redirect("/contacts")
    else:
        return render_template("new.html", contact=new_contact)

@route("/contacts/<contact_id>")
def contacts_view(contact_id: str):
    contact = read({"_id": contact_id})
    return render_template("show.html", contact=contact[0])