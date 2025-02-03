from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
import os
from django.conf import settings



@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user) 
    coin, created = Coin.objects.get_or_create(user=request.user)
    
    # Create a single context dictionary
    context = {
        'user': request.user, 
        'profile_pic': user_profile.profile_pic.url if user_profile.profile_pic else '/media/default.png',
        'total_coins': coin.total_coins,
        'spend_coins': coin.spend_coins,
        'reward_coins': coin.reward_coins
    }

    return render(request, 'profile.html', context)

  
@login_required
def update_profile(request):
    if request.method == 'POST' and request.FILES.get('profile_pic'):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        if user_profile.profile_pic and user_profile.profile_pic.name != './default.png':
            old_path = os.path.join(settings.MEDIA_ROOT, user_profile.profile_pic.name)
            if os.path.isfile(old_path):
                os.remove(old_path)

        user_profile.profile_pic = request.FILES['profile_pic']
        user_profile.save()
    return redirect('profile')


def profile_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('profile')  
    else:
        return redirect('signup') 
    

def coin_history(request):
    history = CoinHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'coin_history.html', {'history': history})
    
