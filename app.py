from flask import Flask, render_template, jsonify
from news_logic import get_articles

app = Flask(__name__)
articles = get_articles()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/news/<int:i>")
def api_news(i):
    article = articles[i % len(articles)]
    return jsonify(article)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)

