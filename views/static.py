import bottle


def stylesheets(filename):
    return bottle.static_file(filename, root='static/css/')


def jscripts(filename):
    return bottle.static_file(filename, root='static/js/')


def images(filename):
    return bottle.static_file(filename, root='static/img/')
