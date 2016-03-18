from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import *


def index(request):
    ideas = Idea.objects.filter(valid=True)
    context = {
        'ideas': ideas
    }
    return render(request, 'index.html', context)


def add(request):
    context = {}

    if not request.session.get('has_session'):
        request.session['has_session'] = True

    if request.method == 'POST':
        form = IdeaForm(request.session.session_key, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your troll has been submited for approval")
            return HttpResponseRedirect(reverse('troll:index'))
    else:
        form = IdeaForm(sessionkey=request.session.session_key)
    context["form"] = form
    return render(request, 'add.html', context)
