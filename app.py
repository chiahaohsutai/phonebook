from flask import Flask, redirect, request, render_template
from db.handlers import read

app = Flask(__name__)
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
