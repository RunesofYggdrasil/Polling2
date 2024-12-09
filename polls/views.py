from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Question, Choice, Vote

# Create your views here.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip=x_forwarded_for.split(',')[0]
    else:
        ip=request.META.get('REMOTE_ADDR')
    return ip

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()  # Retrieve all choices for the question
    return render(request, 'polls/results.html', {'question': question, 'choices': choices})

def index(request):
    latest_questions = Question.objects.all()  # Get all questions
    return render(request, 'polls/index.html', {'latest_questions': latest_questions})

def vote(request, question_id): #tracking votes by IP
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':  # If it's a POST request, process the vote
        selected_choices = request.POST.getlist('choices') #as it processes list of choices, ensures many choices per question functionality
        ip_address = get_client_ip(request)

        if Vote.objects.filter(question=question, ip_address=ip_address).exists(): #error message
            return JsonResponse({"error": "You have already voted!"}, status=403)
        
        for choice_id in selected_choices:
            choice = get_object_or_404(Choice, pk=choice_id, question=question)
            choice.votes +=1
            choice.save()
        
            Vote.objects.create(question=question, choice=choice, ip_address=ip_address)
    
        return redirect('polls:results', question_id=question.id)
    else:  # If it's a GET request, display the results
        return render(request, 'polls/results.html', {'question': question})