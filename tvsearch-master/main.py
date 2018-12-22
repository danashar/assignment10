import os
from bottle import (get, post, request, route, run, static_file, template, error)
import utils
import json


# Static Routes

@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")


@route('/')
def index():
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@route('/ajax/show/<name>')
def routing(name):
    sectionTemplate = "./templates/show.tpl"
    sectionData = json.loads(utils.getJsonFromFile(name))
    return template(sectionTemplate, version=utils.getVersion(), sectionTemplate=sectionTemplate, result=sectionData)


@route('/ajax/show/<name>/episode/<episode>')
def routing(name, episode):
    sectionTemplate = "./templates/episode.tpl"
    sectionData = json.loads(utils.getJsonFromFile(name))

    episodes = sectionData['_embedded']['episodes']
    for episodeData in episodes:
        if episodeData['id'] == int(episode):
            return template(sectionTemplate, version=utils.getVersion(), sectionTemplate=sectionTemplate,
                            result=episodeData)


@error(404)
def error404(error):
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate="./templates/404.tpl",
                    sectionData={})


@route('/show/<name>')
def show(name):
    sectionTemplate = "./templates/show.tpl"
    sectionData = json.loads(utils.getJsonFromFile(name))
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=sectionData)


@route('/show/<name>/episode/<episode>')
def episode(name, episode):
    sectionTemplate = "./templates/episode.tpl"
    sectionData = json.loads(utils.getJsonFromFile(name))

    episodes = sectionData['_embedded']['episodes']
    for episodeData in episodes:
        if episodeData['id'] == int(episode):
            return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                            sectionData=episodeData)

    return error404(None)


@route('/browse')
def browse():
    sectionTemplate = "./templates/browse.tpl"
    sectionData = [json.loads(utils.getJsonFromFile(id)) for id in utils.AVAILABE_SHOWS]
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=sectionData)


@route('/search')
def search():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@route('/search', method='POST')
def search():
    searchQuery = request.forms.get('q')
    results = []

    shows = [json.loads(utils.getJsonFromFile(id)) for id in utils.AVAILABE_SHOWS]
    for show in shows:
        for episode in show['_embedded']['episodes']:
            if episode['name'] is None:
                tmpName = ''
            else:
                tmpName = episode['name']

            if episode['summary'] is None:
                tmpSummary = ''
            else:
                tmpSummary = episode['summary']

            if searchQuery in tmpName or searchQuery in tmpSummary:
                res = {}
                res['showid'] = show['id']
                res['episodeid'] = episode['id']
                res['text'] = show['name'] + ":" + episode['name']
                results.append(res)

    sectionTemplate = "./templates/search_result.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    query=searchQuery, results=results, sectionData={})


run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
