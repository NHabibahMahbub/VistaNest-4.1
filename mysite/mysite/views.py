from django.db.models import Q
from platforms.models import Platform, Bid, Favorite, UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from platforms.forms import SearchForm, BidForm, MarkSoldForm, UserProfileForm, ProfileEditForm, \
    PasswordChangeFormCustom
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


@login_required(login_url='login')
def home(request):
    platform = Platform.objects.all()
    print('>>>>>>>>>>>>', Bid.objects.filter(property=platform[0]))
    for i in platform:

        sort_by = request.GET.get('sort_by', 'title')  # Default sort by 'title'
        sort_order = request.GET.get('sort_order', 'asc')  # Default sort order is ascending

        # Determining the sort order
        if sort_order == 'desc':
            sort_by = f'-{sort_by}'
        platform = Platform.objects.all().order_by(sort_by)

    return render(request, 'home.html', {
        "platform": platform, 'platform_bids': None,
    })


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if all fields are filled
        if not (username and email and password1 and password2):
            messages.error(request, "Please fill out all fields.")
            return redirect("signup")

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        # Check if the password meets security criteria
        if len(password1) < 1:
            messages.error(request, "Password should be at least 1 character.")
            return redirect("signup")

        try:
            my_user = User.objects.create_user(username=username, email=email, password=password1)
            my_user.save()

            UserProfile.objects.create(user=my_user)

            # Log the user in
            login(request, my_user)
            return redirect("home")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect("signup")

    return render(request, 'signup.html')


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    return render(request, 'login.html')


def logoutPage(request):
    logout(request)
    return redirect('login')


def search(request):
    form = SearchForm(request.GET or None)
    results = None

    if form.is_valid():
        query = form.cleaned_data['query']

        results = Platform.objects.filter(
            Q(title__icontains=query) |
            Q(property_type__icontains=query) |
            Q(city__icontains=query) |
            Q(country__icontains=query) |
            Q(location__icontains=query) |
            Q(price__icontains=query)
        )

    return render(request, 'search.html', {
        'form': form,
        'results': results,
    })


def details(request, property_id):
    platform = get_object_or_404(Platform, pk=property_id)
    bids = platform.bids.all().select_related('user')
    return render(request, 'details.html', {
        "platform": platform, 'bids': bids,
    })


def place_bid(request, platform_id):
    platform = get_object_or_404(Platform, id=platform_id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.user = request.user
            bid.property = platform
            bid.save()
            messages.success(request, f'Bid of ${bid.amount} placed successfully!')
            return redirect('home')  # Redirect to the home page or other view as needed
        else:
            messages.error(request, 'There was an issue with your bid.')
    else:
        form = BidForm()

    return render(request, 'forms.html', {'form': form, 'platform': platform})


@login_required
def add_to_favorites(request, platform_id):
    property_obj = get_object_or_404(Platform, id=platform_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, property=property_obj)
    if created:
        message = f"{property_obj.title} has been added to your favorites."
    else:
        message = f"{property_obj.title} is already in your favorites."
    return redirect('favorites')


@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('property')
    return render(request, 'favorites.html', {'favorites': favorites})


@login_required
def unfavorite_property(request, property_id):
    favorite = get_object_or_404(Favorite, user=request.user, property_id=property_id)
    favorite.delete()  # Remove the favorite property
    return redirect('favorites')


def buy_property(request, property_id):
    """Mark a property as sold when purchased"""
    property_obj = get_object_or_404(Platform, id=property_id)

    if property_obj.status == 'sold':
        return redirect('home')

    if request.method == "POST":
        form = MarkSoldForm(request.POST, instance=property_obj)
        if form.is_valid():
            property_obj.mark_as_sold()
            return redirect('home')

    return render(request, 'buy_property.html', {"platform": property_obj})


@login_required
def user_profile(request):
    return render(request, 'user_profile.html')


@login_required
def edit_profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        user_form = ProfileEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('user_profile')

    else:
        user_form = ProfileEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been updated successfully!')
            return redirect('user_profile')
        else:
            messages.error(request, 'There was an error with your password change.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'password_form': form})