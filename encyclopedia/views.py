from django.forms.widgets import HiddenInput
import markdown
import random

from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django import forms
from django.urls import reverse

from . import util


class NewArticleForm(forms.Form):
    title = forms.CharField(label="New Article:", widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg col-md-8 col-lg-6'}))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': '# Title', 'class': 'form-control col-md-8 col-lg-10', 'rows': 10}))
    edit = forms.BooleanField(
        initial=False, widget=forms.HiddenInput(), required=False)


class SearchBar(forms.Form):
    search_field = forms.CharField(label="", widget=forms.TextInput(attrs={
        "placeholder": "Search..."
    }))




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "SearchForm": SearchBar()

    })


def entry(request, title):

    entryFiles = util.get_entry(title)
    if title == "newArticle":
        return newArticle(request)

    if title == "search":
        return search(request)

    if title == "random_page":
        return random_page(request)

    if entryFiles is None:
        return render(request, "encyclopedia/notFoundPage.html", {
            "title": title.capitalize()
        })
    else:
        return render(request, "encyclopedia/entries.html", {
            "entry": markdown.markdown(entryFiles),
            "title": title.capitalize(),
            "SearchForm": SearchBar()
        })


def newArticle(request):
    if request.method == "POST":
        form = NewArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None or form.cleaned_data["edit"] is True:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("index"))
            else:
                error = "The Article that you are trying to create already exists! Try to create a new one!"
                return render(request, "encyclopedia/newArticle.html", {
                    "msg":error,
                    "SearchForm": SearchBar()
                })
        else:
            return render(request, "encyclopedia/newArticle.html", {
                "form": form
            })
    return render(request, "encyclopedia/newArticle.html", {
        "form": NewArticleForm(),
        "SearchForm": SearchBar()
    })


def edit(request, title):
    edit_entry = util.get_entry(title)
    form = NewArticleForm()
    form.fields["title"].initial = title
    form.fields["title"].widget = forms.HiddenInput()
    form.fields["content"].initial = edit_entry
    form.fields["edit"].initial = True
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form,
        "edit": form.fields["edit"].initial,
        "entryPage": form.fields["title"].initial,
        "SearchForm": SearchBar()
    })


def search(request):

    if request.method == "POST":
        search_form = SearchBar(request.POST)

        if search_form.is_valid():
            articleTitle = search_form.cleaned_data["search_field"]
            entrys = util.get_entry(articleTitle)
            if entrys:
                return HttpResponseRedirect(reverse("entry", args=[articleTitle]))
            else:
                search_entries = util.search_entries(articleTitle)
                return render(request, "encyclopedia/search.html", {
                    "search": search_entries,
                    "title": articleTitle,
                    "SearchForm": SearchBar()
                })


def delete(request, title):
    filename = f"entries/{title}.md"
    default_storage.delete(filename)
    return HttpResponseRedirect("/wiki")

def random_page(request):
    rand_title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('entry', args=[rand_title]))