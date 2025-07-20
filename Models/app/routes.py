from flask import Blueprint, render_template, request, redirect, url_for, session
from .chatbot import get_bot_response

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@main.route("/chat", methods=["GET", "POST"])
def chat():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        user_input = request.form["user_input"]
        bot_response = get_bot_response(user_input)
        session["chat_history"].append((user_input, bot_response))
        session.modified = True

    return render_template("chat.html", chat_history=session["chat_history"])
