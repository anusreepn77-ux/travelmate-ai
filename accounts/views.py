from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()
            login(request, user)

            return redirect('user_dashboard')

    else:
        form = UserCreationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


@login_required
def user_dashboard(request):

    return render(
        request,
        'user/dashboard.html'
    )
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .models import TravelPreference


@login_required
def preferences(request):

    preference, created = TravelPreference.objects.get_or_create(
        user=request.user,
        defaults={
            'interests': '',
            'preferred_climate': '',
            'budget': 0,
            'preferred_category': ''
        }
    )

    if request.method == 'POST':

        preference.interests = request.POST.get('interests')
        preference.preferred_climate = request.POST.get('climate')
        preference.budget = request.POST.get('budget')
        preference.preferred_category = request.POST.get('category')

        preference.save()

        messages.success(request, 'Preferences saved successfully!')

        return redirect('user_dashboard')

    return render(
        request,
        'user/preferences.html',
        {'preference': preference}
    )

