from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question,Choice
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
 template_name = "polls/index.html"
 context_object_name = "latest_question_list"
 
 def get_queryset(self): 
  return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class ResultsView(generic.DetailView):
 template_name = "polls/results.html"
 model = Question
 
 def get_queryset(self):
  return Question.objects.filter(pub_date__lte=timezone.now())
 
def vote(request,question_id):
 question = get_object_or_404(Question,pk=question_id)
 try:
  selected_choice = question.choice_set.get(pk=request.POST['choice'])
 except (Choice.DoesNotExist, KeyError):
  context = {'question' : question,
             'error_message' : "No choice selected" }
  return render(request,"polls/detail.html",context)
 else:
  selected_choice.vote += 1
  selected_choice.save()
 return HttpResponseRedirect(reverse('polls:results',args=(question_id,)))

class DetailView(generic.DetailView):
 template_name = "polls/detail.html"
 model = Question
 
 def get_queryset(self):
  return Question.objects.filter(pub_date__lte=timezone.now())
  
