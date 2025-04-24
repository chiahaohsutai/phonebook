from flask import Flask, flash, redirect, render_template, request

from db.handlers import count, delete, insert, read, update
from db.schemas import Contact

app = Flask(__name__)
app.secret_key = b"chia"
route = app.route


@route("/", strict_slashes=False)
def index():
    return redirect("/contacts")


@route("/contacts", strict_slashes=False)
def contacts():
    page = int(request.args.get("page", 1))
    params = (
        {"$sort": {"first": 1, "last": 1}},
        {"$skip": (page - 1) * 10},
        {"$limit": 10},
    )

    if (q := request.args.get("q")) is None:
        contacts = read(*params)
        return render_template("index.html", contacts=contacts, page=page)

    search_query = {"$match": {"$or": [{"first": {"$eq": q}}, {"last": {"$eq": q}}]}}
    if request.headers.get("HX-Trigger") == "search":
        contacts = read(search_query, {"$limit": 10})
        return render_template("rows.html", contacts=contacts, page=page)

    contacts = read(search_query, *params)
    return render_template("rows.html", contacts=contacts, page=page)


@route("/contacts/count", strict_slashes=False)
def contacts_count():
    return f"({count()} total Contacts)"


@route("/contacts/new", methods=["GET"], strict_slashes=False)
def contacts_new_get():
    return render_template("new.html", contact=Contact())


@route("/contacts/new", methods=["POST"], strict_slashes=False)
def contact_new_post():
    form = request.form
    new_contact = Contact(**form.to_dict())
    if insert(new_contact):
        flash("Contact added successfully!", "success")
        return redirect("/contacts", code=303)
    else:
        return render_template("new.html", contact=new_contact)


@route("/contacts/<contact_id>", strict_slashes=False)
def contacts_view(contact_id: str):
    contact = read({"$match": {"_id": contact_id}})
    return render_template("show.html", contact=contact[0])


@route("/contacts/<contact_id>/edit", methods=["GET"], strict_slashes=False)
def contacts_edit_get(contact_id: str):
    contact = read({"$match": {"_id": contact_id}})
    return render_template("edit.html", contact=contact[0])


@route("/contacts/<contact_id>/edit", methods=["POST"], strict_slashes=False)
def contacts_edit_post(contact_id: str):
    form = request.form
    updated_contact = Contact(**form.to_dict())
    updated_contact.id = contact_id

    if update(updated_contact):
        flash("Contact updated successfully!", "success")
        return redirect("/contacts", code=303)
    else:
        return render_template("edit.html", contact=updated_contact)


@route("/contacts/<contact_id>", methods=["DELETE"], strict_slashes=False)
def contacts_delete(contact_id: str):
    if delete(contact_id):
        flash("Contact deleted successfully!", "success")
    else:
        flash("Contact not found!", "error")

    if request.headers.get("HX-Trigger") == "delete-btn":
        return redirect("/contacts", code=303)
    return ""


@route("/contacts/<contact_id>/email", strict_slashes=False)
def contacts_email(contact_id: str):
    if not (email := request.args.get("email")):
        return ""

    contacts = read({"$match": {"email": {"$eq": email}}})
    return "Email already exists" if len(contacts) > 0 else ""


@route("/contacts", methods=["DELETE"], strict_slashes=False)
def contacts_delete_all():
    ids = [i for i in request.form.getlist("selected_contact_ids")]

    if delete(ids) > 0:
        flash("Contacts deleted successfully!", "success")
    else:
        flash("Error deleting contacts!", "error")

    contacts = read({"$sort": {"first": 1, "last": 1}}, {"$limit": 10})
    return render_template("index.html", contacts=contacts, page=1)
