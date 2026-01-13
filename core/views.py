from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.sessions.models import Session

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Enforce Single Admin Rule
            if user.role == 'admin' and CustomUser.objects.filter(role='admin').exists():
                return render(request, 'core/register.html', {
                    'form': form,
                    'error': 'System Limit Reached: Only one administrator is allowed.'
                })
            user.save()
            # login(request, user) # Don't login strictly until approved? 
            # Requirement says "Login after admin approval".
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_approved and not user.is_superuser:
                return render(request, 'core/login.html', {'form': form, 'error': 'Account pending approval.'})
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

from .models import CustomUser, Block

@login_required
def dashboard_view(request):
    user = request.user
    if user.role == 'admin' or user.is_superuser:
        return redirect('admin_dashboard')
    elif user.role == 'candidate':
        return redirect('candidate_dashboard')
    else:
        return redirect('voter_dashboard')

@login_required
def admin_dashboard(request):
    if not (request.user.role == 'admin' or request.user.is_superuser):
        return redirect('dashboard')
    
    # Pendings
    pending_users = CustomUser.objects.filter(is_approved=False)
    
    # Blockchain
    from .blockchain import Blockchain
    if Block.objects.count() == 0:
        Blockchain.create_genesis_block()
        
    blocks = Block.objects.order_by('-index')
    
    context = {
        'pending_users': pending_users,
        'blocks': blocks
    }
    return render(request, 'core/admin_dashboard.html', context)

@login_required
def approve_user(request, user_id):
    if not (request.user.role == 'admin' or request.user.is_superuser):
        return redirect('dashboard')
    
    user = CustomUser.objects.get(id=user_id)
    user.is_approved = True
    user.save()
    return redirect('admin_dashboard')

from .models import SiteConfiguration
from .forms import SiteConfigurationForm
from django.contrib import messages
from voting.models import Vote

@login_required
def superadmin_login(request):
    # Enforce fresh login every time this view is hit
    if 'god_mode_active' in request.session:
        del request.session['god_mode_active']

    if not request.user.is_superuser:
        messages.error(request, "Access Denied.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        password = request.POST.get('password')
        if request.user.check_password(password):
            # Password correct, set session flag
            request.session['god_mode_active'] = True
            return redirect('superadmin_dashboard')
        else:
            messages.error(request, "Incorrect Password.")
            
    return render(request, 'core/superadmin_login.html')

@login_required
def superadmin_dashboard(request):
    # Enforce Superuser Only
    if not request.user.is_superuser:
        messages.error(request, "Access Denied: God Mode requires Superuser privileges.")
        return redirect('dashboard')

    # Enforce Password Re-entry (Sudo Mode)
    if not request.session.get('god_mode_active'):
        return redirect('superadmin_login')

    config = SiteConfiguration.get_solo()
    
    if request.method == 'POST':
    # Handles partial updates by merging current config with POST data
        form_id = request.POST.get('form_id')

        if form_id == 'create_user':
            # Create User Logic
            try:
                username = request.POST.get('username')
                email = request.POST.get('email')
                password = request.POST.get('password')
                role = request.POST.get('role')
                auto_approve = request.POST.get('auto_approve') == 'on'

                if CustomUser.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists.")
                else:
                    user = CustomUser.objects.create_user(username=username, email=email, password=password)
                    user.role = role
                    user.is_approved = auto_approve
                    user.save()
                    messages.success(request, f"User {username} created successfully as {role}.")
            except Exception as e:
                messages.error(request, f"Error creating user: {str(e)}")
            return redirect('superadmin_dashboard')

        elif form_id == 'approve_user':
             # Approve specific user
            try:
                user_id = request.POST.get('user_id')
                user = CustomUser.objects.get(id=user_id)
                user.is_approved = True
                user.save()
                messages.success(request, f"User {user.username} approved.")
            except CustomUser.DoesNotExist:
                messages.error(request, "User not found.")
            return redirect('superadmin_dashboard')
            
        elif form_id == 'delete_user':
             # Delete specific user
            try:
                user_id = request.POST.get('user_id')
                user = CustomUser.objects.get(id=user_id)
                if user.is_superuser:
                     messages.error(request, "Cannot delete Superuser.")
                else:
                    user.delete()
                    messages.success(request, f"User {user.username} deleted.")
            except CustomUser.DoesNotExist:
                messages.error(request, "User not found.")
            return redirect('superadmin_dashboard')

        elif form_id == 'change_password':
            # Change Password Logic
            try:
                user_id = request.POST.get('user_id')
                new_password = request.POST.get('new_password')
                user = CustomUser.objects.get(id=user_id)
                if new_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, f"Password updated for {user.username}.")
                else:
                    messages.error(request, "Password cannot be empty.")
            except CustomUser.DoesNotExist:
                messages.error(request, "User not found.")
            return redirect('superadmin_dashboard')

        elif form_id == 'force_logout':
            user_id = request.POST.get('user_id')
            try:
                # Invalidate Key Sessions
                sessions = Session.objects.filter(expire_date__gte=now())
                logout_count = 0
                for session in sessions:
                    data = session.get_decoded()
                    if str(data.get('_auth_user_id')) == str(user_id):
                        session.delete()
                        logout_count += 1
                messages.success(request, f"User forcibly logged out from {logout_count} active device(s).")
            except Exception as e:
                messages.error(request, f"Logout failed: {str(e)}")
            return redirect('superadmin_dashboard')

        # Existing Config Update Logic
        from django.forms.models import model_to_dict
        # ... (rest of the partial update logic is fine, but we need to ensure it only runs if form_id is config related or default)
        
        # ACTUALLY, simpler structure:
        if form_id in ['general_settings', 'theme_admin', 'theme_voter', 'theme_candidate', 'system_controls', 'dashboard_simulation', 'security_controls']:
            # ... execute config update ...
             # Let's clean up the previous partial logic into a cleaner block
            data = model_to_dict(config)
            for key, value in request.POST.items():
                if key != 'csrfmiddlewaretoken' and hasattr(config, key):
                     # Type conversion logic
                    field = SiteConfiguration._meta.get_field(key)
                    if field.get_internal_type() == 'BooleanField':
                        value = True if value else False
                    elif field.get_internal_type() == 'IntegerField':
                        try:
                            value = int(value)
                        except ValueError:
                            continue 
                    setattr(config, key, value)
            
            # Handle Favicon Upload
            if 'favicon' in request.FILES:
                config.favicon = request.FILES['favicon']
            
            if form_id == 'system_controls':
                config.maintenance_mode = 'maintenance_mode' in request.POST
                config.allow_registration = 'allow_registration' in request.POST
            
            if form_id == 'security_controls':
                config.security_encryption_active = 'security_encryption_active' in request.POST

            config.save()
            messages.success(request, "Configuration Updated.")
            return redirect('superadmin_dashboard')

    else:
        form = SiteConfigurationForm(instance=config)
    
    # Context for User Management
    all_users = CustomUser.objects.exclude(is_superuser=True).order_by('-date_joined')
    
    return render(request, 'core/superadmin_dashboard.html', {'form': form, 'all_users': all_users})

@login_required
def delete_block(request, block_id):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard')
    
    block = get_object_or_404(Block, id=block_id)
    block_index = block.index
    
    # Vote Reversion Logic
    linked_votes = Vote.objects.filter(block_index=block_index)
    deleted_count = linked_votes.count()
    linked_votes.delete()
    
    block.delete()
    
    messages.success(request, f"Block #{block_index} deleted. Reverted {deleted_count} vote(s).")
    return redirect('admin_dashboard')
