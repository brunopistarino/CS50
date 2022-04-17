from django.shortcuts import render, redirect
from markdown2 import markdown
from random import choice

from . import util

# List all the entries

def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

# Render the page of an entry

def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/entry.html", {"title":title, "error":True})
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {"content":content, "title":title})
    
# Search an entry or a group of entries

def search(request):
    search = request.GET.get('q')
    results = []
    if search in util.list_entries():
        return redirect('entry', title=search)
    for entry in util.list_entries():
        if search.lower() in entry.lower():
            results.append(entry)
            empty = False
    if results == []:
        empty = True
    return render(request, "encyclopedia/search.html", {"search":search, "results":results, "empty":empty})

# Create new page

def new(request):
    if request.POST.get('save') == 'save':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title in util.list_entries():
            return render(request, "encyclopedia/new.html", {"error":"This title is the same as another page, try another.", "title":title, "content":content})
        if title == "":
            return render(request, "encyclopedia/new.html", {"error":"The page title can't be empty.", "title":title, "content":content})
        util.save_entry(title, bytes(content, 'utf8')) # saved as bytes to solve a problem with extra lines in the md file
        return redirect("entry", title=title)
    return render(request, "encyclopedia/new.html")

# Edit existing page

def edit(request, title):
    content = util.get_entry(title)
    if request.POST.get('savechanges') == 'savechanges':
        content = request.POST.get('content')
        util.save_entry(title, bytes(content, 'utf8')) # saved as bytes to solve a problem with extra lines in the md file
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {"content":content, "title":title})

# Redirect to a random page

def random(request):
    return redirect("entry", title=choice(util.list_entries()))