from flask import Flask, render_template, url_for, request
import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
client = MongoClient(os.getenv("MONGODB_URI"))
app.db = client.microblog


@app.route("/", methods=["GET", "POST"])
def index():
    print([e for e in app.db.entries.find({})])
    if request.method == "POST":
        entry_content = request.form.get("content")
        formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
        app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

    entries_with_date = [
            (entry["content"], entry["date"], datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"))
            for entry in app.db.entries.find({})
        ]

    return render_template('index.html', entries=entries_with_date)


if __name__ == '__main__':
    app.run(debug=True)

    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )
