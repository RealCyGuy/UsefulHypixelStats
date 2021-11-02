import os

import flask
from flask import Flask, render_template, request
from dotenv import load_dotenv
import hypixel
import requests
from flask_assets import Environment

load_dotenv()

hypixel.setKeys(os.environ.get("HYPIXEL_KEYS").split(","))
app = Flask(__name__)
assets = Environment(app)


@app.route("/")
def index():
    if request.args.get("search"):
        return flask.redirect("/" + request.args.get("search"))
    return render_template("index.html")


@app.route("/<user>")
def profile(user):
    r = requests.get("https://playerdb.co/api/player/minecraft/" + user)
    r = r.json()
    if not r["success"]:
        return render_template("notfound.html", name=user)
    username = r["data"]["player"]["username"]
    if username != user:
        return flask.redirect("/" + username)
    try:
        player = hypixel.Player(r["data"]["player"]["id"])
    except hypixel.PlayerNotFoundException:
        return render_template("notonhypixel.html", name=username)
    return render_template(
        "profile.html",
        player=player,
        json=player.JSON,
        image=r["data"]["player"]["avatar"],
        name=username,
    )
