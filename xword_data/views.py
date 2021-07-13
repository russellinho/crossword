from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, response
from django.template.defaulttags import register
from .models import Clue, Entry, Puzzle

def drill(request):
    # if no clue provided, get a random one
    clueId = request.GET.get('clue_id', -1)
    context = {}
    if clueId == -1:
        # get random clue
        clue = Clue.objects.order_by("?").first()
        # present random clue to user
        context = {
            "clue_id": clueId,
            "clue_text": clue.clue_text,
            "clue_len": len(clue.entry.entry_text),
            "puzzle_title": clue.puzzle.title
        }
        return HttpResponseRedirect('/?clue_id=' + str(clue.id))
    else:
        # if a clue id is provided, render it
        clue = None
        try:
            clue = Clue.objects.get(id=clueId)
        except:
            return HttpResponse(status=404)

        context = {
            "clue_id": clueId,
            "clue_text": clue.clue_text,
            "clue_len": len(clue.entry.entry_text),
            "puzzle_title": clue.puzzle.title
        }
        # render whether or not the provided guess was incorrect if it was incorrect
        fail = request.GET.get('fail', 0)
        if fail == "1":
            messages.error(request, "This answer is incorrect!")

    # return request
    return render(request, "base.html", context)

def answer(request):
    myAnswer = request.GET.get('answer', None)
    clueId = request.GET.get('clue_id', None)
    if clueId == None:
        return HttpResponseRedirect('/')
    
    correctAnswer = None
    try:
        correctAnswer = Clue.objects.get(id=clueId)
    except:
        return HttpResponse(status=404)

    context = {}

    # if gave up, get the right answer and move onto the answer reveal page
    if myAnswer == None:
        counts = {}
        cluesList = []
        relatedClues = Clue.objects.filter(clue_text=correctAnswer.clue_text)
        for c in relatedClues:
            if c.entry.entry_text in counts:
                counts[c.entry.entry_text] = counts[c.entry.entry_text] + 1
            else:
                counts[c.entry.entry_text] = 1
                cluesList.append(c.entry.entry_text)
        context = {
            "success": 0,
            "answer": correctAnswer.entry.entry_text,
            "clues": cluesList,
            "counts": counts
        }
        context["resMessage"] = "only appearance of this clue" if len(cluesList) == 1 else "multiple appearances"
    elif myAnswer == correctAnswer.entry.entry_text:
        # if successful guess, move onto the answer reveal page
        counts = {}
        cluesList = []
        relatedClues = Clue.objects.filter(clue_text=correctAnswer.clue_text)
        for c in relatedClues:
            if c.entry.entry_text in counts:
                counts[c.entry.entry_text] = counts[c.entry.entry_text] + 1
            else:
                counts[c.entry.entry_text] = 1
                cluesList.append(c.entry.entry_text)
        context = {
            "success": 0,
            "answer": correctAnswer.entry.entry_text,
            "clues": cluesList,
            "counts": counts
        }
        context["resMessage"] = "only appearance of this clue" if len(cluesList) == 1 else "multiple appearances"
    else:
        # if unsuccessful guess, redirect back to the guess page
        return HttpResponseRedirect('/?clue_id=' + str(clueId) + "&fail=1")

    return render(request, "answer.html", context)

@register.filter
def get_item(dictionary, key):
    return dictionary[key]
