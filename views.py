from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Group, Message
from .forms import UserRegistrationForm, GroupCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Group, Message
from .forms import GroupCreationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('group_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('group_list')
        else:
            messages.error(request, 'Login failed. Please check your username and password.')
    return render(request, 'registration/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def group_list(request):
    user = request.user
    joined_groups = user.members.all()
    # groups = Group.objects.all()
    return render(request, 'group/group_list.html', {'groups': joined_groups})

@login_required
def group_chat(request, group_id):
    group = Group.objects.get(id=group_id)
    messages = Message.objects.filter(group=group)
    if request.method == 'POST':
        content = request.POST['content']
        if content.strip():  # Check if the message content is not empty
            Message.objects.create(user=request.user, group=group, content=content)
            return redirect('group_chat', group_id=group_id)
    return render(request, 'group/group_chat.html', {'group': group, 'messages': messages})



@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.members.add(request.user)
    messages.success(request, f'You have joined the group: {group.name}')
    return redirect('group_list')

@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.members.remove(request.user)
    messages.success(request, f'You have left the group: {group.name}')
    return redirect('group_list')

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save()
            group.members.add(request.user)
            messages.success(request, f'Group "{group.name}" created successfully.')
            return redirect('group_list')
    else:
        form = GroupCreationForm()
    
    return render(request, 'group/create_group.html', {'form': form})

# @login_required
# def group_chat(request, group_id):
#     group = get_object_or_404(Group, id=group_id)
#     messages = Message.objects.filter(group=group)
#     if request.method == 'POST':
#         content = request.POST['content']
#         if content.strip():
#             Message.objects.create(user=request.user, group=group, content=content)
#             return redirect('group_chat', group_id=group_id)
#     return render(request, 'group/group_chat.html', {'group': group, 'messages': messages})

@login_required
def group_members(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    members = group.members.all()
    return render(request, 'group/group_members.html', {'group': group, 'members': members})
