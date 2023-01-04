from django.shortcuts import render, redirect
from .forms import CreateNewsForm
from django.contrib import messages
from django.template.defaultfilters import slugify
from .models import News, SubscribedMails
from .utils import send_news_letter

# Create your views here.

def newsFeed(request):
    news = News.objects.all().order_by('-updated_at')[:5]
    context = {
        'news':news,
    }
    return render(request,'newsletter/newsFeed.html',context)

def addNews(request):
    form = CreateNewsForm()
    if request.method=="POST":
        form = CreateNewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.created_by = request.user
            news.slug = 'temp'
            news.save()
            news.slug = slugify(form.cleaned_data['title']+'-'+str(news.id))
            news.save()
            send_news_letter(news)
            messages.success(request,'News has been posted to newsletter successfully!')
            return redirect('newsFeed')
        else:
            messages.error(request,'Validation Error')
            
    context = {
        'form':form,
    }
    return render(request,'newsletter/add_news.html',context)


def fullNews(request,news_slug):
    news = News.objects.get(slug=news_slug)
    context = {
        'news':news,
    }
    return render(request,'newsletter/full_news.html',context)

def updateNews(request,news_slug):
    news = News.objects.get(slug=news_slug)
    form = CreateNewsForm(instance=news)
    if request.method=="POST":
        form = CreateNewsForm(request.POST, instance=news)
        if form.is_valid():
            news = form.save(commit=False)
            news.created_by = request.user
            news.slug = slugify(form.cleaned_data['title']+'-'+str(news.id))
            news.save()
            send_news_letter(news)
            messages.success(request,'News has been posted to newsletter successfully!')
            return redirect('newsFeed')
        else:
            messages.error(request,'Validation Error')
            
    context = {
        'form':form,
    }
    return render(request,'newsletter/add_news.html',context)

def deleteNews(request,news_id):
    if request.user.is_admin:
        news = News.objects.get(id=news_id)
        messages.success(request,f'"{news.title}" news deleted successfully')
        news.delete()
    else:
        messages.warning(request,'Only admin can delete the order')
    return redirect('newsFeed')

def unsubscribe(request):
    if request.POST:
        email = request.POST.get('email')
        if SubscribedMails.objects.filter(email=email).count() == 1:
            user = SubscribedMails.objects.get(email=email)
            user.is_active=False
            user.save()
            messages.success(request,'You have unsubscribed to foodOnline Newsletter')
            return redirect('home')
        else:
            messages.error(request,'This email address is not subscribed at foodOnline')
            return redirect('unsubscribe')
    return render(request,'newsletter/unsubscribe.html')
    
    

