from flask import Flask, flash, redirect, render_template, request
from uuid import uuid4

from db.handlers import delete, insert, read, update
from db.schemas import Contact

app = Flask(__name__)
app.secret_key = uuid4().bytes
route = app.route


@route("/", strict_slashes=False)
def index():
    return redirect("/contacts")


@route("/contacts", strict_slashes=False)
def contacts():
    if not (q := request.args.get("q")):
        contacts = read()
    else:
        conditions = [{"first": {"$eq": q}}, {"last": {"$eq": q}}]
        contacts = read({"$or": conditions})

    return render_template("index.html", contacts=contacts)


@route("/contacts/new", methods=["GET"], strict_slashes=False)
def contacts_new_get():
    return render_template("new.html", contact=Contact())


@route("/contacts/new", methods=["POST"], strict_slashes=False)
def contact_new_post():
    form = request.form
    new_contact = Contact(**form.to_dict())
    if insert(new_contact):
        flash("Contact added successfully!", "success")
        return redirect("/contacts")
    else:
        return render_template("new.html", contact=new_contact)


@route("/contacts/<contact_id>", strict_slashes=False)
def contacts_view(contact_id: str):
    contact = read({"_id": contact_id})
    return render_template("show.html", contact=contact[0])


@route("/contacts/<contact_id>/edit", methods=["GET"], strict_slashes=False)
def contacts_edit_get(contact_id: str):
    contact = read({"_id": contact_id})
    return render_template("edit.html", contact=contact[0])


@route("/contacts/<contact_id>/edit", methods=["POST"], strict_slashes=False)
def contacts_edit_post(contact_id: str):
    form = request.form
    updated_contact = Contact(**form.to_dict())
    updated_contact.id = contact_id

    if update(updated_contact):
        flash("Contact updated successfully!", "success")
        return redirect("/contacts")
    else:
        return render_template("edit.html", contact=updated_contact)


@route("/contacts/<contact_id>/delete", methods=["POST"], strict_slashes=False)
def contacts_delete(contact_id: str):
    if delete(contact_id):
        flash("Contact deleted successfully!", "success")
    else:
        flash("Contact not found!", "error")
    return redirect("/contacts")
