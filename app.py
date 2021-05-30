from flask import Flask, render_template, request
import urllib.request
import re
import random
from markupsafe import Markup

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xf0\xac\x82\x18\n\xc5\xd6\xd6\xfak\xbei\x92\xc0\xaf\xad{\xf3\xc1\x96\xef"\x9ct'

def search(video):
    html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={video}&sp=CAM%253D")
    code = html.read().decode()
    videoIDs = re.findall(r"watch\?v=(\S{11})", code)
    return "https://www.youtube.com/embed/"+ random.choice(videoIDs)

def make_url(raw_query):
    query = raw_query.replace('_', '+')
    query = raw_query.replace(' ', '+')
    url = search(query)
    return url

@app.route("/", strict_slashes=False)
def home():
    return render_template('home.html')

@app.route("/about", strict_slashes=False)
def about():
    return render_template('about.html')

@app.route("/watch", strict_slashes=False)
def watch():
    raw_query = request.args.get("query")
    if raw_query:
        url = make_url(raw_query)
        return render_template("watch.html", link=Markup(f'<iframe src={url} allowfullscreen height=\'600px\' width=\"100%\" frameborder=\"0\"></iframe>')) 
    return render_template("watch.html")

if __name__ == "__main__":
    app.run()

