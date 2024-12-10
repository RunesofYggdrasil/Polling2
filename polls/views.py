from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from matplotlib.style import context
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
from .models import Question, Choice, Vote

# Create your views here.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip=x_forwarded_for.split(',')[0]
    else:
        ip=request.META.get('REMOTE_ADDR')
    return ip

def get_graph(question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = [choice for choice in Choice.objects.all() if choice.question == question]
    labels = [choice.choice_text for choice in choices]
    votes = [choice.votes for choice in choices]

    fig = plt.figure()
    plt.bar(range(len(choices)), votes, tick_label = labels, width = 0.2, color = "purple")

    plt.xlabel("Meals")
    plt.ylabel("Votes")
    plt.title(question.question_text)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = [choice for choice in Choice.objects.all() if choice.question == question]  # Retrieve all choices for the question
    graph = get_graph(question_id)
    return render(request, 'polls/results.html', {'question': question, 'choices': choices, 'graph': graph})

def index(request):
    data = [get_graph(1), get_graph(2), get_graph(3)]
    questions = Question.objects.all()  # Get all questions
    choices = {}
    for question in questions:
        questr = str(question)
        for choice in Choice.objects.all():
            if choice.question == question:
                choice_id = ''.join([c.lower() if c.isalnum() else '_' for c in choice.choice_text])
                if questr in choices:
                    choices[questr].append({choice_id: choice})
                else:
                    choices[questr] = [{choice_id: choice}]
    return render(request, 'polls/index.html', {'choices': choices, 'bf_graph': data[0], "ln_graph": data[1], "dn_graph": data[2]})

@csrf_exempt
def vote(request, question_id): #tracking votes by IP
    question = get_object_or_404(Question, pk=question_id)
    meals = ["Breakfast", "Lunch", "Dinner"]
    if request.method == 'POST':  # If it's a POST request, process the vote
        selected_choices = request.POST.getlist(meals[question_id - 1].lower()) #as it processes list of choices, ensures many choices per question functionality
        print(selected_choices)
        ip_address = get_client_ip(request)

        if Vote.objects.filter(user_ip=ip_address).exists(): #error message
            return JsonResponse({"error": "You have already voted!"}, status=403)
        
        for choice_txt in selected_choices:
            choice = get_object_or_404(Choice, choice_text=choice_txt, meal=meals[question_id - 1])
            choice.votes += 1
            choice.save()
        
            Vote.objects.create(choice=choice, user_ip=ip_address)
    
        return redirect('polls:results', question_id=question.id)
    else:  # If it's a GET request, display the results
        return render(request, 'polls/results.html', {'question': question})