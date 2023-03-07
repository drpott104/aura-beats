from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Mood, User
from datetime import date

def home(request):
  return render(request, 'home.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid credientals, please try again'
  form = UserCreationForm()
  context = { 'form': form, 'error_message': error_message }
  return render(request, 'registration/signup.html', context)

def about(request):
    return render(request, 'about.html')

@login_required
def moods_index(request):
  moods = Mood.objects.all().order_by('-id').values()
  return render(request, 'moods/index.html', { 'moods': moods })

@login_required
def moods_detail(request, mood_id):
    mood = Mood.objects.get(id=mood_id)
    return render(request, 'moods/detail.html', {
       'mood': mood
    })

def favorites(request, mood_id):
    mood = get_object_or_404(Mood, pk=mood_id)
    if mood.favorites.filter(id=request.user.ide).exist():
        mood.favorites.remove(request.user)
    else:
        mood.favorites.add(request.user)
    return render(request, 'favorites/mood_favorite_list.html')

def mood_favorite_list(request, id):
    user=request.user
    favorite_moods = user.favorites.all()
    context = {
        'favorite_moods': favorite_moods
    }
    return render(request, 'favorites/mood_favorite_list.html', context)

@login_required
def my_moods(request):
  userz = request.user
  moods_list = Mood.objects.filter(user=request.user).order_by('-id').values()
  return render(request, 'main_app/mood_list.html', { 'moods': moods_list, 'user': userz})

class MoodCreate(CreateView):
  model = Mood
  fields = ['name', 'description']

  def form_valid(self, form):
    form.instance.user = self.request.user

    return super().form_valid(form)

class MoodUpdate(UpdateView):
    model = Mood
    fields = ['description']

class MoodDelete(DeleteView):
    model = Mood
    success_url = '/moods'