from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomRegistrationForm
from orders.models import Order
from .models import Profile

# 1. មុខងារឡុកអ៊ីន
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard_user')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# 2. មុខងារចុះឈ្មោះ
def register_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard_user')
    else:
        form = CustomRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

# 3. មុខងារចាកចេញ
def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('/')


# 4. User Dashboard
@login_required(login_url='login')
def user_dashboard(request):
    """User dashboard displaying profile and order history"""
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    
    # Calculate user statistics
    total_orders = orders.count()
    total_spent = sum(order.total for order in orders)
    
    # Get recent orders (last 5)
    recent_orders = orders[:5]

    # Try to find a phone number from the most recent order that includes it
    phone = None
    recent_with_phone = orders.filter(phone__isnull=False).exclude(phone='')
    if recent_with_phone.exists():
        phone = recent_with_phone.first().phone
    else:
        # no phone in orders — leave empty (do not expose email as phone)
        phone = ''

    # ensure profile available for templates
    profile, _ = Profile.objects.get_or_create(user=user)
    
    context = {
        'user': user,
        'orders': orders,
        'recent_orders': recent_orders,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'phone': phone,
        'profile': profile,
    }
    return render(request, 'accounts/user_dashboard.html', context)


@login_required(login_url='login')
def user_profile(request):
    """User profile view with edit functionality"""
    user = request.user
    # ensure profile exists
    profile, _ = Profile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        # Handle password change
        if 'change_password' in request.POST:
            current_password = request.POST.get('current_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            
            # Verify current password
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
            elif new_password1 != new_password2:
                messages.error(request, 'New passwords do not match.')
            elif len(new_password1) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
            else:
                user.set_password(new_password1)
                user.save()
                messages.success(request, 'Password changed successfully!')
                # Log the user back in
                login(request, user)
        else:
            # Handle profile update
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            # phone handled on profile
            phone_val = request.POST.get('phone', profile.phone)
            profile.phone = phone_val
            profile.save()
            user.save()
            messages.success(request, 'Profile updated successfully!')
    
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'accounts/user_profile.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    """User order detail view"""
    order = Order.objects.get(id=order_id, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'accounts/order_detail.html', context)