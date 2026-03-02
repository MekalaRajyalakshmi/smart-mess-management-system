from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from logic.models import Menu, Confirmation, Profile
from datetime import date
from django.db.models import Count
from functools import wraps
from django.contrib.auth import logout


# --- REGISTRATION LOGIC ---
def register_view(request):

    # Redirect already logged-in users to their dashboard
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        role = request.POST.get('role')

        if form.is_valid() and role:
            user = form.save()

            Profile.objects.create(
                user=user,
                role=role
            )

            login(request, user)

            # Role based redirect after registration
            if role == 'student':
                return redirect('studentdashboard')
            elif role == 'cook':
                return redirect('cookdashboard')
            elif role == 'rep':
                return redirect('repsdashboard')

            return redirect('home')

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


# --- ROLE-BASED ACCESS HELPERS ---
def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect('login')

            profile = getattr(request.user, 'profile', None)

            if profile and profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            return render(request, '403.html', status=403)

        return _wrapped_view
    return decorator


@login_required
def dashboard_redirect(request):

    profile = getattr(request.user, 'profile', None)

    if not profile:
        return redirect('register')

    role = profile.role

    if role == 'cook':
        return redirect('cookdashboard')

    if role == 'rep':
        return redirect('repsdashboard')

    return redirect('studentdashboard')


# --- COOK MODULE ---
@login_required
@role_required(['cook'])
def cookdashboard(request):

    if request.method == 'POST':
        date_val = request.POST.get('date')
        meal_type = request.POST.get('meal_type')
        items = request.POST.get('items')

        if date_val and meal_type and items:
            Menu.objects.update_or_create(
                date=date_val,
                meal_type=meal_type,
                defaults={'items': items}
            )

    menus = Menu.objects.filter(date__gte=date.today()).order_by('date')

    return render(request, 'cookdashboard.html', {'menus': menus})


# --- STUDENT MODULE ---
@login_required
@role_required(['student'])
def studentdashboard(request):

    today = date.today()
    menus = Menu.objects.filter(date=today)

    if request.method == 'POST':
        meal_type = request.POST.get('meal_type')
        will_eat = request.POST.get('will_eat') == 'yes'

        if meal_type:
            Confirmation.objects.update_or_create(
                user=request.user,
                date=today,
                meal_type=meal_type,
                defaults={'will_eat': will_eat}
            )

    user_confirms = Confirmation.objects.filter(user=request.user, date=today)
    status_map = {c.meal_type: c.will_eat for c in user_confirms}

    for menu in menus:
        menu.attendance_status = status_map.get(menu.meal_type)

    return render(request, 'studentdashboard.html', {
        'menus': menus,
    })


# --- REP MODULE ---
@login_required
@role_required(['rep'])
def repsdashboard(request):

    today = date.today()

    stats = (
        Confirmation.objects
        .filter(date=today, will_eat=True)
        .values('meal_type')
        .annotate(count=Count('id'))
    )

    return render(request, 'repsdashboard.html', {
        'stats': stats,
        'today': today
    })
def logout_view(request):
    logout(request)
    return redirect('login')