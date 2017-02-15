from django.test import TestCase
from django.utils import timezone
from .models import Question
import datetime
from django.urls import reverse

class QuestionMethodTests(TestCase):
 
 def test_was_published_recently_with_future_question(self):
  future_question = Question.objects.create(question_text="whats new?",pub_date=timezone.now()+datetime.timedelta(days=30))  
  self.assertIs(future_question.was_published_recently(),False)
  
 def test_was_published_recently_with_previous_question(self):
  previous_question = Question(pub_date=timezone.now() - datetime.timedelta(days=15))
  self.assertIs(previous_question.was_published_recently(),False)
  
 def test_was_published_recently_with_recent_question(self):
  recent_question = Question(pub_date=timezone.now()-datetime.timedelta(hours=1))
  self.assertIs(recent_question.was_published_recently(),True)
  
def create_question(question_text,days):
  time = timezone.now()+datetime.timedelta(days=days)
  return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionViewTests(TestCase):
  
 def test_with_no_questions(self):
  response = self.client.get(reverse('polls:index'))
  self.assertEqual(response.status_code,200)
  self.assertContains(response,"No polls available.")
  self.assertQuerysetEqual(response.context['latest_question_list'],[])

 def test_with_question_previous_date(self):
  create_question("whats new?",-30)
  response = self.client.get(reverse('polls:index'))
  self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: whats new?>'])
  
 def test_with_question_future_date(self):
  create_question("how do?",30)
  response = self.client.get(reverse('polls:index'))
  self.assertQuerysetEqual(response.context['latest_question_list'],[])
  
 def test_with_question_previous_future_date(self):
  create_question("hello 1",-12)
  create_question("hello 2",12)
  response = self.client.get(reverse('polls:index'))
  self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: hello 1>'])
  
 def test_with_question_previous_two_dates(self):
  create_question("hello 1",-12)
  create_question("hello 2",-14)
  response = self.client.get(reverse('polls:index'))
  self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: hello 1>','<Question: hello 2>'])
  #self.assertQuerysetEqual(response.context['latest_question_list'],[])

class QuestionIndexDetailTests(TestCase):
 
 def test_with_pub_date_future(self):
  future_question = create_question(question_text="hello 1",days=5)
  response = self.client.get(reverse('polls:detail',args=(future_question.id,)))
  self.assertEqual(response.status_code,404)

 def test_with_pub_date_previous(self):
  future_question = create_question(question_text="hello 1",days=-15)
  response = self.client.get(reverse('polls:detail',args=(future_question.id,)))
  self.assertEqual(response.status_code,200)
  self.assertContains(response,future_question.question_text)
  
# class QuestionIndexChoiceTests(TestCase):

 # def test_without_choices(self):
  # question = create_question(question_text='hello 1',days=-15)
  # question.choice_set.create(choice_text='choice 1')
  # question.choice_set.create(choice_text='choice 2')
  # question.choice_set.create(choice_text='choice 3')
  # question.choice_set.create(choice_text='choice 4')
  # response = self.client.get(reverse('polls:index'))
  # self.assertEqual(response.status_code,200)
 
 
