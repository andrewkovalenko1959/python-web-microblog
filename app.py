from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient

# added def create_app():
# to avoid multiple deployment put next line, app factory
def create_app():


    app = Flask(__name__)
    client = MongoClient("mongodb+srv://andrey:eUQVbeB5AP6pSUTh@microblog-application.x58ex.mongodb.net/test",
                         ssl=True, ssl_cert_reqs='CERT_NONE')

    # client = MongoClient("mongodb+srv://andrey:eUQVbeB5AP6pSUTh@microblog-application.x58ex.mongodb.net/test", ssl=True)
    # https://pymongo.readthedocs.io/en/stable/examples/tls.html
    app.db = client.microblog
    entries = []


    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/304
    @app.route("/", methods=["GET", "POST"])  # we need to tell flask we are getting a POST
    def home():
            # print([e for e in app.db.entries.find({})])

            if request.method == "POST":
                entry_content = request.form.get("content")
                # "content " is an area in html , form and we removed action="/entry "
                formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
                # print(entry_content, datetime.datetime.now())
                # print(entry_content, datetime.datetime.today())
                # entries.append((entry_content, formatted_date))
                app.db.entries.insert({"content": entry_content, "date": formatted_date})

                # print(entries)
            entries_with_date = [
                (
                    entry["content"],
                    entry["date"],
                    datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
                )
                for entry in app.db.entries.find({})
            ]
            return render_template("home.html", entries=entries_with_date)

    return app
