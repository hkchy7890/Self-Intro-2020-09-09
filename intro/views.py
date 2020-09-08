from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EnquiryForm, PostForm
from .models import Post, Like, Poll
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def mainpage(request):
    return render(request, 'mainpage.html')

def login_view(request):
    form = AuthenticationForm()
    context = {
        'form': form
    }
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect('/')
        else:
            messages.info(request, 'Username OR Password is incorrect')
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def about(request):
    return render(request, 'about.html')

def whyit(request):
    return render(request, 'whyit.html')

def photos(request):
    return render(request, 'photos.html')

#@login_required(login_url='/login')
def contact(request):
    form = EnquiryForm()
    context = {
        'form': form
    }
    if request.method == "POST":
        form = EnquiryForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Thank you for comment!')
        else:
            messages.info(request, 'Name or Comment Field should be not empty')
    return render(request, 'contact.html', context)

def create_post(request):
    return render(request, 'createpost.html')

def posts_all(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts
    }
    return render(request, 'posts.html', context)

def like_post(request):
    user = request.user
    if request.method == 'POST':
        page = request.POST.get('page_num')
        #print('like page: ' + page)
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)
        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()
    if page == "":
        return HttpResponseRedirect('/posts')
    else:
        re = '/posts?page=' + str(page)
        return HttpResponseRedirect(re)

def polls_main(request):
    polls = Poll.objects.all()
    context = {
        'polls': polls
    }
    return render(request, 'polls.html', context)

def poll_vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == "POST":
        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        elif selected_option == 'option4':
            poll.option_four_count += 1
        else:
            return HttpResponse(400, "Invalid form")
        poll.save()
        relink = "/results/" + poll_id
        return redirect(relink)

    context = {
        'poll': poll
    }
    return render(request, 'poll_vote.html', context)


def poll_results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll': poll
    }
    return render(request, 'poll_results.html', context)