# Traceback handler for python
import cgi
import cgitb
import json
import time
from os import listdir
from os.path import isfile, join
import urllib.parse

cgitb.enable()

POSTS_PATH = "posts/"

def printHead(title):
        print("""Content-type: text/html\n
        <!DOCTYPE html>
        <html lang="de">
        <head>
        <meta charset="utf-8">
        <title>{}</title></head>""".format(title))

def printFooter():
    print("""
    <a href="posts-create.py>New Post</a>
    <a href="tags-show.py">Show tags</a>
    </body></html>""")

def printPosts(posts, tagFilter=None):
    print("<body>")

    if tagFilter: 
        for p in posts:
            if tagFilter in p["tags"]:
                print("""
                <h1>{}</h1>
                <h4>{}</h4>
                <p>{}</p>
            """.format(p["title"], p["published"], p["content"]))
            for t in p["tags"]:
                safeTag = urllib.parse.quote(t, safe='')
                print("<a href=tags-show.py?tag={}>{}</a>".format(safeTag, "#"+safeTag))
            printFooter()
    else: 
        # Ugly copy paste....
        if len(posts) == 0:
            print("Noch keine Posts vorhanden ...")
        else: 
            for p in posts:
                print("""
                    <h1>{}</h1>
                    <h4>{}</h4>
                    <p>{}</p>
                """.format(p["title"], p["published"], p["content"]))
                for t in p["tags"]:
                    safeTag = urllib.parse.quote(t, safe='')
                    print("<a href=tags-show.py?tag={}>{}</a>".format(safeTag, "#"+safeTag))
        printFooter()

# Liefert die aktuelle Uhrzeit im Format Jahr-Monat-Tag-Stunde-Minute-Sekunde
def get_timestamp():
    return time.strftime("%Y-%m-%d-%H-%M-%S")

# Writes post as json ecnoded file
def writePost(filename, post):
    # Speichere das Dictionary JSON-codiert
    with open(join(POSTS_PATH, filename), 'w') as outfile:
        json.dump(post, outfile)

# Liest den json-codiert gespeicherten Task mit Dateiname filename ein
def readPost(filename):
    # Öffne den JSON-codierten Task
    with open(join(POSTS_PATH, filename), 'r') as json_file:
        # Decodiere die JSON-Datei in ein Dictionary
        return json.load(json_file)


# Reads all saved posts
def readAllPosts():
    # Returns all files in our POSTS_PATH
    file_names = [f for f in listdir(POSTS_PATH) if isfile(join(POSTS_PATH, f))]

    # Read all found posts
    posts = [readPost(f) for f in file_names]

    # Sort posts by title 
    sorted_posts = sorted(posts, key=lambda t: t["published"], reverse=False)

    return sorted_posts


def create_post(title, content, tags):
    timestamp = get_timestamp()
    # First entry is an empty string, so remove it and split tags with list comprehension
    tagsSplit = [x.replace("#", "") for x in tags.split("#")][1:]

    post = {
        "title": title,
        "published": timestamp,
        "tags": tagsSplit,
        "content": content
    }
    # Write json file
    writePost(timestamp, post)
    return post


def printTags(posts):
    tags = {}
    for p in posts:
        for t in p["tags"]:
            tags.add(t)
    print("<body>")
    for t in tags:
        safeTag = urllib.parse.quote(t, safe='')
        print("<a href=tags-show.py?tag={}>{}</a>".format(safeTag, "#"+safeTag))
    printFooter()

# Creates HTTP-Redirect
def redirect(location):
    print("Status: 303 See Other")
    print("Location: {}".format(location))
    print()

def printErrorPage(title, message, exception):
    printHead(title)
    print("<body><p>{}</p>".format(message))
    # Exception ausgeben
    print(repr(exception))
    print("</body></html>")
