# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

from django.db import models
from .models import Character, Quote, DatabaseStats

import random
import json
import bcrypt

# Create your views here.
def index(request):

    error = " LIST:"

    try:
        options_paragraphs = 5
        quotes = []
        character_ids = ['1','2','3','4','5','6','7','8','9','10',
                        '11','12','13','14','15','16','17','18','19','20',
                        '21','22','23','24','25','26','27','28','29','30',
                        '31','32','33','34','35','36']

        if 'character_ids' in request.session:
            character_ids = request.session['character_ids']
            error += "(char_id if)"

        if 'paragraphs' in request.session:
            options_paragraphs = int(request.session['paragraphs']) * 10

        quote_ids = set()
        list_full = False

        temp_quotes = Quote.objects.filter(character__in=character_ids)
        temp_count = len(temp_quotes) - 1

        # Check to see if available quotes is less than user request
        if temp_count < options_paragraphs:
            options_paragraphs = temp_count
            error += "(temp < options)"

        # If no results, skip loop and return nothing.  
        if temp_count <= 0:
            list_full = True
            error += "(temp < 0)"

        while list_full == False: 
            
            r = random.randint(0,temp_count)

            if r not in quote_ids:
                if options_paragraphs != 0:

                    quotes.append(temp_quotes[r].text)

                    options_paragraphs = options_paragraphs - 1
                else:
                    list_full = True
                
                quote_ids.add(r)

        # Update generated texts count
        gen_count = DatabaseStats.objects.get(id=1)
        gen_count.count += 1
        gen_count.save()

        error += "(DatabaseStat error)"
        
        context = {
            "count": DatabaseStats.objects.get(id=1),
            "quotes": json.dumps(quotes)
        }

        return render (request,"main/index.html", context)

    except:
        return HttpResponse("Index render failed " + error)

# Generate process, gather form data and pass to index which retrieves the Queryset
def generate(request):

    request.session['paragraphs'] = request.POST.get('paragraphs')
    
    if 'headers' in request.POST:
        request.session['headers'] = True
    
    if 'lists' in request.POST:
        request.session['lists'] = True

    ids = []
    # Add all selected characters from page to use to filter the database
    for i in range(1,36):
        if str(i) in request.POST:
            ids.append(str(i))

    request.session['character_ids'] = ids

    return redirect("home")

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