from django.http import HttpResponse
from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from random import choice

from . import util

class NewPageBox(forms.Form):
    title = forms.CharField() 
    content = forms.CharField(widget=forms.Textarea(attrs={'style':'width: 60%; height: 50%;'}))

def index(request):
    entries = util.list_entries()
    if request.method == 'POST':
        inp=request.POST
        title = inp['q']
        if title in entries:
            return display_page(request, title)
        else:
            others = []
            for entry in entries:
                if title in entry:
                    others.append(entry)
            return render(request, "encyclopedia/index.html", {
            "entries": others, 
        })

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })

def display_page(request, title):
    page = util.get_entry(title)
    if page==None:
        return render(request, "encyclopedia/errorPage.html", {
            "error_message" : "Requested page is not found"
        })
    markdown = Markdown()
    html_page = markdown.convert(page)
    return render(request, "encyclopedia/page.html", {
        "title" : title,
        "content" : html_page,
    })

def random(request):
    entries = util.list_entries()
    title = choice(entries)
    return display_page(request, title)

def new_page(request):
    entries = util.list_entries()
    if request.method == 'POST':
        form = NewPageBox(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in entries:
                return render(request, "encyclopedia/errorPage.html", {
                    "error_message" : "Page with title already exists"
                })
            else:
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                return display_page(request, title)
        else:
            return render(request, "encyclopedia/newPage.html", {
            'type' : "New",
            'form' : form
        })
    
    else:
        return render(request, "encyclopedia/newPage.html", {
            'type' : "New",
            'form' : NewPageBox()
        })
    
def edit(request):
    inp = request.POST
    title = inp["title"]
    content = util.get_entry(title)
    return render(request, "encyclopedia/editPage.html", {
        'type' : "Edit",
        'form' : NewPageBox(initial={"title":title, "content":content})
    })

def save_edit(request):
    if request.method == 'POST':
        form = NewPageBox(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            util.save_entry(title, content)
            return display_page(request, title)
    