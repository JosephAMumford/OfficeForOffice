# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from .models import Character, Quote, DatabaseStats

import random
import json
import bcrypt

# Create your views here.
def index(request):
    return render (request,"main/index.html")

@csrf_exempt
def get_quotes(request):
    quotes = []
    paragraphs = request.POST.get("paragraphs")
    headers = request.POST.get("headers")
    lists = request.POST.get("lists")
    characters = []

    for i in range(1,36):
        if request.POST.get(str(i)) == 'true':
            characters.append(str(i))

    quote_ids = set()
    list_full = False

    temp_quotes = Quote.objects.filter(character__in=characters)
    temp_count = len(temp_quotes) - 1

    # Check to see if available quotes is less than user request
    if temp_count < paragraphs:
        paragraphs = temp_count

    # If no results, skip loop and return nothing.  
    if temp_count <= 0:
        list_full = True

    while list_full == False: 
        
        r = random.randint(0,temp_count)

        if r not in quote_ids:
            if paragraphs != 0:

                quotes.append(temp_quotes[r].text)

                paragraphs = paragraphs - 1
            else:
                list_full = True
            
            quote_ids.add(r)

    # Update generated texts count
    gen_count = DatabaseStats.objects.get(id=1)
    gen_count.count += 1
    gen_count.save()

    return HttpResponse(json.dumps(quotes), content_type="application/json")

# Get generation count
def get_count(request):
    data = {
        'count': DatabaseStats.objects.get(id=1).count
    }
    return HttpResponse(json.dumps(data), content_type="application/json")

# Login Page
def login(request):
    return render(request, "main/login.html")

# Process Login information
def process_login(request):
    
    db = DatabaseStats.objects.get(id=1)
    password = request.POST.get("password")

    if bcrypt.hashpw(password.encode(), db.password.encode()) != db.password:
        return redirect("home")
    else:
        context = {
            'content': Quote.objects.last(),
        }   
        return render(request, "main/add.html", context)

# Process to add quote to database
def add_quote(request):

    quote = request.POST.get("quote")
    character = Character.objects.get(id=request.POST.get("character"))
    season = request.POST.get("season")
    episode = request.POST.get("episode")
    Quote.objects.create(text=quote,season=season,episode=episode,character=character)

    t = DatabaseStats.objects.get(id=1)
    t.records = t.records + 1  
    t.save() 

    return redirect("add")

# Add Page
def add(request):
    context = {
        'content': Quote.objects.last(),
    }   
    return render(request, "main/add.html", context)

