from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import *
from Dashboard.models import *
from django.contrib.auth.decorators import login_required



def category_view(request):
    categories = Category.objects.all()
    return render(request,'category.html',{'categories':categories})


def topic_view(request,category_name):
    category = get_object_or_404(Category, name=category_name)
    topics = Topic.objects.filter(category=category)
    return render(request, 'topic.html', {'category': category, 'topics': topics})

@login_required
def lesson_view(request, category_name, topic_name):
    category = get_object_or_404(Category, name=category_name)
    topic = get_object_or_404(Topic, name=topic_name, category=category)
    lessons = Lesson.objects.filter(topic=topic)
    return render(request, 'lesson.html', {'category': category,'topic': topic, 'lessons': lessons})

def lesson_detail(request, category_name, topic_name, lesson_name, view_type='document'):
    # Fetch the category, topic, and lesson objects from the database
    category = get_object_or_404(Category, name=category_name)
    topic = get_object_or_404(Topic, name=topic_name, category=category)
    lesson = get_object_or_404(Lesson, name=lesson_name, topic=topic)
    
    # Retrieve all lessons for the topic, ordered by their ID
    lessons = Lesson.objects.filter(topic=topic).order_by('id')
    
    # Find the current lesson index
    lesson_index = list(lessons).index(lesson)
    
    # Get or create a Coin object for the current user
    coin, _ = Coin.objects.get_or_create(user=request.user)

    if request.method == 'POST':  # Handle the form submission when the "Complete" button is clicked
        if lesson.is_completed:
            messages.error(request, "Lesson already completed. Coins have already been added.")
        else:
            # Mark the lesson as completed
            lesson.is_completed = True
            lesson.save()

            # Add 10 coins to the user's account as a reward
            coin.add_reward_coins(10)

            # Record this in the CoinHistory for auditing purposes
            CoinHistory.objects.create(user=request.user, coin_type="reward", amount=10)

            messages.success(request, "Lesson completed! You earned 10 coins.")

            # Redirect back to the lesson page to avoid resubmitting the form on refresh
            return HttpResponseRedirect(reverse('lesson_detail', kwargs={
                'category_name': category.name,
                'topic_name': topic.name,
                'lesson_name': lesson.name,
                'view_type': view_type,
            }))
    
    # Set the previous and next lesson (if any)
    previous_lesson = lessons[lesson_index - 1] if lesson_index > 0 else None
    next_lesson = lessons[lesson_index + 1] if lesson_index < len(lessons) - 1 else None
    
    # Determine which template to use based on view_type
    template = 'lesson_video.html' if view_type == 'video' else 'lesson_document.html'

    # Render the lesson detail page with the necessary context
    return render(request, template, {
        'category': category,
        'lesson': lesson,
        'lessons': lessons,
        'topic': topic,
        'view_type': view_type,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
        'current_lesson': lesson
    })