import json
import re
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
import datetime


def welcome(request):
    return HttpResponseRedirect("/news/")


def get_article(request, link):
    with open(settings.NEWS_JSON_PATH, 'r') as f:
        posts = json.load(f)
    post = next(item for item in posts if item["link"] == link)
    return render(request, "../templates/news/news.html", {'post': post})


def sort_dates(json_data):
    list_dates = []
    for i in json_data:
        list_dates.append(i["created"].split()[0])
    the_list = list(dict.fromkeys(list_dates))
    the_list.sort()
    the_list.reverse()
    return the_list


def get_search(json_data, pattern):
    search_list = []
    for article in json_data:
        if re.search(pattern, article["title"], re.IGNORECASE):
            search_list.append(article)
    return search_list


def index(request):
    with open(settings.NEWS_JSON_PATH, 'r') as json_obj:
        json_data = json.load(json_obj)
    sorted_dates = sort_dates(json_data)
    pattern_search = request.GET.get('q')
    if pattern_search:
        json_data = get_search(json_data, pattern_search)
    news = {}
    for date in sorted_dates:
        for article in json_data:
            if date == article["created"].split()[0]:
                if date in news.keys():
                    news[date].append(article)
                else:
                    news[date] = [article]
    return render(request, "../templates/news/index.html", {"news": news})


def create(request):
    if request.method == "GET":
        return render(request, "../templates/news/new_article.html")
    else:
        with open(settings.NEWS_JSON_PATH, "r") as json_obj:
            json_data = json.load(json_obj)
        title = request.POST.get("title")
        text = request.POST.get("text")
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        link = int(datetime.datetime.timestamp(datetime.datetime.now()))

        new_article = {
            "created": date,
            "text": text,
            "title": title,
            "link": link
        }
        json_data.append(new_article)
        with open(settings.NEWS_JSON_PATH, "w") as json_obj:
            json.dump(json_data, json_obj)

        return HttpResponseRedirect("/news/")
