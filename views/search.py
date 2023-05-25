import bottle


def search():
    search = bottle.template("search")
    return bottle.template("base", {"body": search})
