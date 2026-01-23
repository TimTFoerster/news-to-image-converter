from flask import Flask, jsonify, render_template
from news_logic import process_article, news_feed

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/news/<int:i>")
def get_news(i):
    entry_no = i % len(news_feed.entries)
    article = process_article(entry_no)
    return jsonify(article)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
