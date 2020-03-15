from bottle import (
    route, run, template, request, redirect
)
from bayes import NaiveBayesClassifier, clean
from scraputils import get_news
from db import News, session
import bottle

@bottle.route('/')
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('./news_template.tpl', rows=rows)


@route("/add_label/")
def add_label():

    s = session()
    id = request.query.id
    label = request.query.label
    news = s.query(News).get(id)
    news.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():

    s = session()
    base = s.query(News).all()
    new_news = get_news('https://news.ycombinator.com/', 3)
    for i in new_news:
        for j in base:
            if (i['title'] == j.title) and (i['author'] == j.author):
                break
            else:
                news = News(title=i['title'],
                            author=i['author'],
                            url=i["url"],
                            comments=i['comments'],
                            points=i['points'])
                s.add(news)
                s.commit()
    redirect("/news")

@route("/classify")
def classify_news():

    s = session()
    none_news = []
    rows = s.query(News).filter(News.label == None).all()
    learn_news = s.query(News).filter(News.label != None).all()
    X_train, y_train = [], []
    for news in learn_news:
        X_train.append(news.title)
        y_train.append(news.label)
    X_train = [clean(x).lower() for x in X_train]
    model = NaiveBayesClassifier(alpha=1)
    model.fit(X_train, y_train)
    for news in rows:
        none_news.append(news.title)
    predict_labels = model.predict(none_news)
    for news, label in zip(rows, predict_labels):
        news.label = label
    classified_news = sorted(rows, key=lambda news: news.label)
    return template('./news_recommendations.tpl', rows=classified_news)



if __name__ == "__main__":
    run(host="localhost", port=8080)
