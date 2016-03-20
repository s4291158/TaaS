from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

from .forms import *


def index(request):
    context = {}

    if not request.session.get('has_session'):
        request.session['has_session'] = True

    if request.method == 'POST':
        idea_id = request.POST['idea_id']
        form = LikeForm(request.session.session_key, idea_id, request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({})

    context['ideas_tuple'] = []
    ideas = Idea.objects.filter(valid=True)
    for idea in ideas:
        session, is_new = Session.objects.get_or_create(key=request.session.session_key)
        likes = Like.objects.filter(idea=idea, session=session)
        if not is_new and len(likes) == 1 and likes[0].liked:
            already_liked = True
        else:
            already_liked = False
        context['ideas_tuple'].append((idea, already_liked))

    likeform = LikeForm(sessionkey=request.session.session_key)
    context['likeform'] = likeform
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
            return HttpResponseRedirect(reverse('troll:vote'))
    else:
        form = IdeaForm(sessionkey=request.session.session_key)
    context["form"] = form
    return render(request, 'add.html', context)


def vote(request):
    context = {}

    if not request.session.get('has_session'):
        request.session['has_session'] = True

    if request.method == 'POST':
        idea_id = request.POST['idea_id']
        form = LikeForm(request.session.session_key, idea_id, request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({})

    context['ideas_tuple'] = []
    ideas = Idea.objects.filter(valid=True)
    for idea in ideas:
        session, is_new = Session.objects.get_or_create(key=request.session.session_key)
        likes = Like.objects.filter(idea=idea, session=session)
        if not is_new and len(likes) == 1 and likes[0].liked:
            already_liked = True
        else:
            already_liked = False
        context['ideas_tuple'].append((idea, already_liked))

    likeform = LikeForm(sessionkey=request.session.session_key)
    context['likeform'] = likeform

    return render(request, 'vote.html', context)
